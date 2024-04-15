---
layout: page
title: Disguised Face Recognition
description: Recognizing faces with intentional/unintentional disguising effects
importance: 2
category: research
---

#### Problem Definition
Recognizing a person’s face images with intentional/unintentional disguising effects such as make-up,
plastic surgery, artificial wearables (hats, eye-glasses) is a challenging task, termed as Disguised Face Recognition (DFW).
Recently, this task has gained attention because of the pandemic situation where people are wearing masks.  

#### Approach
In this project, We propose a **F**eature **E**nsem**B**le **N**etwork (FEBNet) for recognizing Disguised Faces in the
Wild (DFW). FEBNet encompasses multiple base networks (SE-ResNet50, Inception-ResNet-V1) pretrained on large-scale face recognition datasets (MS-Celeb-1M, VGGFace2)
and fine-tuned on DFW training dataset.

##### Acknowledgements
This project was done as part of my internship at Computer Vision Lab, IIT Madras under the guidance of [Dr Anurag Mittal](http://www.cse.iitm.ac.in/~amittal/). You can find the research paper explaining the methods and experiments <a href="/assets/pdf/febnet.pdf">here</a>.  