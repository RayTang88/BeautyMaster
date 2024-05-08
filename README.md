# BeautyMaster

We hope to train VLM to be a beauty master to help you solve the problem of dressing and beauty.


## 💪 Goal

Welcome Pull request！！！

Project stages:
- Primary
1. Train a VLM to have basic aesthetic ability.
2. Align human aesthetic abilities.
3. Choose the right match according to aesthetic ability.
4. The previous results are presented through pictures.


## ✊ Todo

#### Train a VLM to have basic aesthetic ability
- [x] Data Processing(WIP)
  - [x] Collect fashion wear data
  - [x] Look for a VLM to label ready-made images [internVL](https://internvl.opengvlab.com/)

#### Align human aesthetic abilities

- [ ] RLHF [instruct](https://arxiv.org/pdf/2203.02155.pdf)
- [ ] DPO [DPO](https://arxiv.org/abs/2305.18290)
- [ ] ORPO [ORPO](https://arxiv.org/abs/2403.07691)(https://github.com/xfactlab/orpo/tree/main)
- [ ] RLHF-V [RLHF-V](https://arxiv.org/abs/2312.00849)(https://github.com/RLHF-V/RLHF-V)

#### Choose the right match according to aesthetic ability.

- [ ] The trained VLM gives suggestions on what to wear [internVL](https://internvl.opengvlab.com/)


#### The previous results are presented through pictures

- [ ] Segment Tool
  - [ ] [segment-anything](https://github.com/facebookresearch/segment-anything): **Features**: it can be used to generate masks for all objects in an image.
  - [ ] [Self Correction for Human Parsing](https://github.com/TannedCung/SCHP)**Features**: An out-of-box human parsing representation extractor.
- [ ] Virtual Try-on
  - [ ] [IDM-VTON](https://github.com/yisol/IDM-VTON): **Features**: it could keep background of the VToN, **Techs**: IP-Adapter, TryonNet, GarmentNet
  - [ ] [COTTON-size-does-matter](https://github.com/cotton6/COTTON-size-does-matter): **Features**: it can adjust the size of VToN with a parameter
  - [ ] [OOTDiffusion](https://github.com/levihsu/OOTDiffusion): **Techs**: LDM-based, outfitting UNet, outfitting dropout, Classifier-free guidance
  - [ ] [OutfitAnyone](https://github.com/HumanAIGC/OutfitAnyone): Ultra-high quality virtual try-on for Any Clothing and Any Person (Including **Anime character pictures** in demo)
  - [ ] [StableVITON](https://github.com/rlawjdghek/StableVITON): **Features**: it could keep background of the VToN, **Techs**: LDM-based, zero cross-attention blocks, attention total variation loss and augmentation,

- [ ] Visualize the results of the suggestions to the user
  - [ ] [ControlNet](https://github.com/lllyasviel/ControlNet)
  - [ ] [4d-dress](https://github.com/eth-ait/4d-dress): A **4D** Dataset of Real-world Human Clothing with **Semantic Annotations**
  - [ ] [champ](https://github.com/fudan-generative-vision/champ): Controllable and Consistent Human **Image Animation with 3D** Parametric Guidance


## 📂 Repo structure (WIP)

```Bash
├── README.md
├── docs
├── scripts
├── beautymaster
│   ├── datasets
│   ├── models
│   │   ├── internvl
│   │   ├── IDM-VTON                     
│   │   ├── champ
│   │   ├── archpp
│   │   ├── ControlNet
│   │   └── OOTDiffusion
│   ├── demo
│   ├── train     
│   └── utils
├── requirements.txt
```

## 🛠️ Requirements and Installation

1. Clone this repository and open BeautyMaster folder
```
git clone https://github.com/RayTang88/BeautyMaster.git
cd BeautyMaster
```
2. Install required packages
```
conda create -n beautyMaster python=3.10 -y
conda activate beautyMaster

```
3. Install additional packages for training cases
```
pip install -r requirements.txt

```


### Datasets
Refer to [Data.md](docs/Data.md)


### Infer

Example:

```Python
cd beautymaster
python demo/infer.py 
```


## 🔒 License
**Usage and License Notices:** The data, code, and checkpoint are intended and licensed for research use only,non-commercial use. They are also restricted to uses that follow the license agreement of InternVL, RLHF,DPO,ORPO,RLHF-V,segment-anything,SCHP,IDM-VTON,ControlNet,4d-dress,champ. The dataset is CC BY NC 4.0 (allowing only non-commercial use) and models trained using the dataset should not be used outside of research purposes.

