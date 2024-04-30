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
- [ ] Collect fashion wear data
- [ ] Look for a VLM to label ready-made images [internVL](https://internvl.opengvlab.com/)

#### Align human aesthetic abilities
- [ ] RLHF [instruct](https://arxiv.org/pdf/2203.02155.pdf)

#### Choose the right match according to aesthetic ability.
- [ ] The trained LLM gives suggestions on what to wear [internVL](https://internvl.opengvlab.com/)


#### The previous results are presented through pictures
- [ ] Segment Tool
  - [ ] [segment-anything](https://github.com/facebookresearch/segment-anything)
- [ ] Virtual Try-on
  - [ ] [IDM-VTON](https://github.com/yisol/IDM-VTON)
  - [ ] [COTTON-size-does-matter](https://github.com/cotton6/COTTON-size-does-matter)
  - [ ] [OOTDiffusion](https://github.com/levihsu/OOTDiffusion)
  - [ ] [OutfitAnyone](https://github.com/HumanAIGC/OutfitAnyone)
  - [ ] [StableVITON](https://github.com/rlawjdghek/StableVITON)
- [ ] Visualize the results of the suggestions to the user
  - [ ] [champ](https://github.com/fudan-generative-vision/champ)
  - [ ] [4d-dress](https://github.com/eth-ait/4d-dress)


## 📂 Repo structure (WIP)
```
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
python demo/infer.py 
```


## 🔒 License
* See [LICENSE](LICENSE) for details.

