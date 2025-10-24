---
layout: distill
title: "InsectAgent: mobile insect recognition with VLM and on-device vision"
description: A walkthrough of how the InsectAgent app blends a classic vision model with a lightweight multimodal model (FastVLM) to identify insects on your iPhone, and only “thinks harder” when it needs to.
date: 2025-10-23
tags: computer-vision, deep-learning, insects, education
giscus_comments: false
featured: false

bibliography: 2025-10-23-insectagent.bib

toc:

  - name: Introduction
  - name: What is InsectAgent?
  - name: InsectAgent Pipeline
  - name: Results
  - name: Video demo
  - name: Conclusion & next steps

---

InsectAgent was presented at ISVLSI 2025 <d-cite key="zhao2025insectagent"></d-cite>. This post gives a brief overview of **InsectAgent**, a small, on-device iOS app that recognizes insects and only “calls in” extra reasoning using a **Multimodal Large Language Model (MLLM/VLM)** when the photo is tricky.

This post is designed for readers with little to no coding experience. We’ll keep things visual and plain-language, and focus on the *why* and *how* of the app’s hybrid pipeline on iPhone.

I hope you find this exploration both accessible and useful!

## Introduction

> Field reality: cell coverage can be patchy (or nonexistent) around traps and plots. When your model depends on the network, everything from retries to latency becomes unpredictable. That’s why **running locally** matters here, beyond privacy alone.

Spotting and identifying insects early can protect crops, reduce chemical sprays, and improve our understanding of seasonal dynamics. The challenge on mobile is achieving **good accuracy with reliable, offline behavior**.

**InsectAgent** takes a pragmatic approach:

1. **Fast local guess**: a compact image classifier runs on-device and proposes likely species.
2. **Think harder only if needed**: a lightweight multimodal model (FastVLM <d-cite key="vasu2025fastvlm"></d-cite>) compares the photo against short species cues to resolve tough look-alikes.

The result feels snappy on easy photos and smarter on ambiguous ones—**no cloud round-trips** and no dependency on spotty field networks.

---

## What is InsectAgent?

**InsectAgent** is an iOS app (Swift/Xcode) (<a href="https://github.com/ajaynarayanan/InsectAgent">code</a>) that demonstrates **hybrid insect recognition** on modern iPhones:

* A **ResNet-18** classifier <d-cite key="he2016deep"></d-cite> provides **top-k** candidates quickly.
* **FastVLM** <d-cite key="vasu2025fastvlm"></d-cite>, a small multimodal LLM, is engaged **only when the classifier isn’t confident**, using brief, visual-first species descriptions (color patterns, wing venation, antenna shape, etc.) to reason about which candidate fits the image best.

**Why this design?**

* Many photos are “easy wins”, the correct class is confidently top-1.
* For borderline cases, the right class often sits *in* the top-k; a little **text-guided reasoning** helps pick the winner.
* Doing this **conditionally** keeps the common case fast while improving the hard cases.

---

## InsectAgent Pipeline

<div class="col-sm mt-3 mt-md-0 text-center">
  <img src="/assets/blogs/insect_agent/insect_agent_pipeline.png"
       class="img-fluid rounded z-depth-1"
       alt="InsectAgent pipeline">
  <div class="caption mt-2 text-center">
    Fig. 1: InsectAgent pipeline. A fast vision model proposes candidates; a VLM is used, only when needed, to compare the image against compact species cues.
  </div>
</div>

### Pipeline components (at a glance)

**1) Vision model → top-k logits**
A compact CNN (say, ResNet-18) produces logits and a ranked list of species candidates. If the **top-1 confidence ≥ τ** (a configurable threshold), we return that label immediately.

**2) Dynamic information augmentation (conditional)**
If confidence is **low**, the system fetches **short, visual-first cue cards** for the top-k species (e.g., “yellow-black banding,” “hind-wing ocelli,” “clubbed antennae”) from a knowledge base.

**3) Multimodal reasoning**
A MLLM compares the input image with those cue cards, weighs evidence, and selects the best match—often correcting near-misses among visually similar species.

---

## Results

### On-device variants (FastVLM<d-cite key="vasu2025fastvlm"></d-cite>) on iPhone 16 Pro (8 GB RAM)

<p><em>100 random insect images from IP102<d-cite key="wu2019ip102"></d-cite>; average end-to-end latency includes conditional runs when triggered. “Out of Memory” means the variant exceeded practical memory limits for our setup.</em></p>

<table>
<thead>
<tr>
  <th style="text-align:left;">Method</th>
  <th style="text-align:right;">Latency (s)</th>
  <th style="text-align:right;">Accuracy (%)</th>
</tr>
</thead>
<tbody>
<tr>
  <td>ResNet-18<d-cite key="he2016deep"></d-cite> only</td>
  <td style="text-align:right;">0.150</td>
  <td style="text-align:right;">46.47</td>
</tr>
<tr>
  <td>ResNet-18 + FastVLM 0.5B</td>
  <td style="text-align:right;">3.016</td>
  <td style="text-align:right;">51.18</td>
</tr>
<tr>
  <td>ResNet-18 + FastVLM 1.5B</td>
  <td style="text-align:right;">7.205</td>
  <td style="text-align:right;">57.06</td>
</tr>
<tr>
  <td>ResNet-18 + FastVLM 7B</td>
  <td style="text-align:right;">Out of Memory</td>
  <td style="text-align:right;">Out of Memory</td>
</tr>
</tbody>
</table>

**Notes.**

* The threshold **τ** governs how often the VLM is invoked: higher τ → more VLM calls (better accuracy, higher latency); lower τ → fewer calls (faster, slightly lower accuracy).
* The **0.5B** and **1.5B** VLMs provide a meaningful accuracy bump over vision-only while remaining feasible on device.
* For broader benchmarks and ablations (e.g., different top-k sizes, cue length), see the paper <d-cite key="zhao2025insectagent"></d-cite>.

---

## Video demo

<div class="col-sm mt-3 mt-md-0 text-center">
  <img src="/assets/blogs/insect_agent/insect_agent_demo.gif"
       class="img-fluid rounded z-depth-1"
       alt="InsectAgent demo">
  <div class="caption mt-2 text-center">
    Fig. 2: Demo of the conditional pipeline in action on an iPhone 16 Pro.
  </div>
</div>

---

## Conclusion & next steps

Pairing a **fast vision model** with **conditional multimodal reasoning** gives the best of both worlds on mobile: quick answers when the photo is clear and expert-like judgment when species look alike—**without relying on flaky field networks**.

**What’s next:**

* **Richer cue cards** — concise, visual-first snippets per class (color/venation/antennae/legs).
* **More classes & field data** — expand coverage and robustness with diverse outdoor images.
* **Explainability UI** — “why not *this* species?” side-by-side comparisons to aid learning and trust.
* **Lightweight field guides** — offline mini-guides for common pests and pollinators.
