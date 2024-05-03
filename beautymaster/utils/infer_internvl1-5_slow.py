from transformers import AutoTokenizer, AutoModel
import torch
import torchvision.transforms as T
from PIL import Image

from torchvision.transforms.functional import InterpolationMode



IMAGENET_MEAN = (0.485, 0.456, 0.406)
IMAGENET_STD = (0.229, 0.224, 0.225)


def build_transform(input_size):
    MEAN, STD = IMAGENET_MEAN, IMAGENET_STD
    transform = T.Compose([
        T.Lambda(lambda img: img.convert('RGB') if img.mode != 'RGB' else img),
        T.Resize((input_size, input_size), interpolation=InterpolationMode.BICUBIC),
        T.ToTensor(),
        T.Normalize(mean=MEAN, std=STD)
    ])
    return transform


def find_closest_aspect_ratio(aspect_ratio, target_ratios, width, height, image_size):
    best_ratio_diff = float('inf')
    best_ratio = (1, 1)
    area = width * height
    for ratio in target_ratios:
        target_aspect_ratio = ratio[0] / ratio[1]
        ratio_diff = abs(aspect_ratio - target_aspect_ratio)
        if ratio_diff < best_ratio_diff:
            best_ratio_diff = ratio_diff
            best_ratio = ratio
        elif ratio_diff == best_ratio_diff:
            if area > 0.5 * image_size * image_size * ratio[0] * ratio[1]:
                best_ratio = ratio
    return best_ratio


def dynamic_preprocess(image, min_num=1, max_num=6, image_size=448, use_thumbnail=False):
    orig_width, orig_height = image.size
    aspect_ratio = orig_width / orig_height

    # calculate the existing image aspect ratio
    target_ratios = set(
        (i, j) for n in range(min_num, max_num + 1) for i in range(1, n + 1) for j in range(1, n + 1) if
        i * j <= max_num and i * j >= min_num)
    target_ratios = sorted(target_ratios, key=lambda x: x[0] * x[1])

    # find the closest aspect ratio to the target
    target_aspect_ratio = find_closest_aspect_ratio(
        aspect_ratio, target_ratios, orig_width, orig_height, image_size)

    # calculate the target width and height
    target_width = image_size * target_aspect_ratio[0]
    target_height = image_size * target_aspect_ratio[1]
    blocks = target_aspect_ratio[0] * target_aspect_ratio[1]

    # resize the image
    resized_img = image.resize((target_width, target_height))
    processed_images = []
    for i in range(blocks):
        box = (
            (i % (target_width // image_size)) * image_size,
            (i // (target_width // image_size)) * image_size,
            ((i % (target_width // image_size)) + 1) * image_size,
            ((i // (target_width // image_size)) + 1) * image_size
        )
        # split the image
        split_img = resized_img.crop(box)
        processed_images.append(split_img)
    assert len(processed_images) == blocks
    if use_thumbnail and len(processed_images) != 1:
        thumbnail_img = image.resize((image_size, image_size))
        processed_images.append(thumbnail_img)
    return processed_images


def load_image(image_file, input_size=448, max_num=6):
    image = Image.open(image_file).convert('RGB')
    transform = build_transform(input_size=input_size)
    images = dynamic_preprocess(image, image_size=input_size, use_thumbnail=True, max_num=max_num)
    pixel_values = [transform(image) for image in images]
    pixel_values = torch.stack(pixel_values)
    return pixel_values

path = "/root/model/InternVL-Chat-V1-5-Int8"
# If you have an 80G A100 GPU, you can put the entire model on a single GPU.
model = AutoModel.from_pretrained(
    path,
    torch_dtype=torch.bfloat16,
    low_cpu_mem_usage=True,
    trust_remote_code=True,
    load_in_8bit=True).eval()


tokenizer = AutoTokenizer.from_pretrained(path, trust_remote_code=True)
# set the max number of tiles in `max_num`


# JSON data
const_prompt="""{
    "id": "<random_number_string>",
    "image": "<image_name>",
    "conversations": [
        {
        "from": "human",
        "value": "<image>\nDescribe this image."
        },
        {
        "from": "gpt",
        "value": "<answer1>"
        },
        {
        "from": "human",
        "value": "What kind of clothing is it, T-shirts, shirts, skirts, whatever?"
        },

        {
        "from": "gpt",
        "value": "<answer2>"
        },
        {
        "from": "human",
        "value": "Describe the details of the dress. Is it off-shoulder?"
        },
        {
        "from": "gpt",
        "value": "<answer3>"
        },
        {
        "from": "human",
        "value": "Describe the style of clothing. Casual, formal?"
        },
        {
        "from": "gpt",
        "value": "<answer4>"
        },
        {
        "from": "human",
        "value": "What color are the clothes?"
        },
        {
        "from": "gpt",
        "value": "<answer5>"
        },
        {
        "from": "human",
        "value": "Is it printed? If yes, please indicate what type of print, text, log?"
        },
        {
        "from": "gpt",
        "value": "<answer6>"
        },
        {
        "from": "human",
        "value": "What is the material of the clothes?"
        },
        {
        "from": "gpt",
        "value": "<answer7>"
        },
        {
        "from": "human",
        "value": "Is it long sleeve or short sleeve?"
        },
        {
        "from": "gpt",
        "value": "<answer8>"
        },

    ]
}"""

# Converts JSON data to a string and escapes double quotes and curly braces
json_string = const_prompt.replace('"', '\\"').replace('{', '\\{').replace('}', '\\}').replace('\n', '\\n')

# Embed the escaped JSON string in the prompt
prompt = f"Create a data set for me in the following format:\n {json_string} \nRequest: Questions and answers, please generate to me. Questions and answers should tightly grasp the content of the image itself, must be strictly from the image content, can not make up, if the image is not, please answer do not know."


generation_config = dict(
    num_beams=1,
    max_new_tokens=512,
    do_sample=False,
)
image_counts=[]
images = []
for i in range(3):
    pixel_values1 = load_image('/root/data/b17ab66100f34037b1a83e4c9e7c97a4_th.jpg', max_num=6).to(torch.bfloat16).cuda()

    image_counts.append(pixel_values1.size(0))
    images.append(pixel_values1)
pixel_values = torch.cat(images, dim=0)

questions = [prompt] * len(image_counts)
responses = model.batch_chat(tokenizer, pixel_values,
                             image_counts=image_counts,
                             questions=questions,
                             generation_config=generation_config)
for question, response in zip(questions, responses):
    print(response)
