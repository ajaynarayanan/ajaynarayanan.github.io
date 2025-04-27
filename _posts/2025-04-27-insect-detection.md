---
layout: distill
title: "AI for insect detection & classification"
description: A simple, visual walkthrough of how AI can spot and identify insects using motion detection and YOLO.
date: 2025-04-27
tags: computer-vision, deep-learning, insects, education
giscus_comments: true
featured: false

bibliography: 2025-04-27-insect-detection.bib

toc:
  - name: Introduction
  - name: Motion detection for insects
  - name: Insect detection with YOLO
  - name: Conclusion & next steps
---


After conducting the [AI for Insect Detection & Classification Workshop](https://insectnet.psu.edu/student-resources/sp25-virtual-workshop-ai-for-insect-detection-classification)<d-cite key="insectnetworkshop2025"></d-cite> at The Pennsylvania State University, I felt motivated to share some of the key ideas more widely. 

This blog post is designed for readers with little to no coding experience. The goal is to explain how simple motion detection and modern object detection models like YOLO<d-cite key="redmon2016you"></d-cite> can be used to monitor insects — using visuals and plain language, without diving into heavy math or programming details. Images and videos used in the blog are obtained from the InsectEye<d-cite key="homan2023insecteye"></d-cite> system. 

I hope you find this exploration both accessible and interesting!


## Introduction

Step into a field at dawn, and you’ll hear a quiet symphony of tiny wings.  
Some belong to helpful pollinators 🐝, while others are hungry pests 🐛.  

Catching these insects early can protect crops, reduce chemical sprays, and help us understand how seasons and climate shape insect life. But how do you do that without draining batteries or overwhelming tiny edge devices?

We use a **two-step camera system** that’s smart and simple:

1. **Notice insect motion** — “Something moved.”  
2. **Detect pests with YOLO** — “Which insect is it?”

Let’s dive into how motion spotting and fast object detection help keep a watchful eye on the fields — one tiny wingbeat at a time.

---

## Motion detection for insects

<div class="col-sm mt-3 mt-md-0 text-center">
  <img src="/assets/blogs/insect_detection/motion_detection/insect.gif" 
       class="img-fluid rounded z-depth-1" 
       style="transform: rotate(180deg); margin-bottom: 20px;" 
       alt="Insect GIF">
  <br>
  <img src="/assets/blogs/insect_detection/motion_detection/motion_masks.gif" 
       class="img-fluid rounded z-depth-1" 
       style="transform: rotate(180deg);" 
       alt="Motion Mask GIF">
</div>
<div class="caption mt-2 text-center">
  Fig. 1: Animated GIFs showing the insect video sequence (top) and the corresponding motion masks (bottom).
</div>

When a camera sits still, most of the scene stays the same. If a handful of pixels suddenly change, that signals **motion**. Here’s a simple background subtraction method to pick out moving insects:

<ol>
  <li>
    <strong>Build a background model</strong><br>
    Watch the scene for a few seconds with no insects, then average those frames to create a ‘clean’ background image. Alternatively, use a single snapshot without any bugs.
    <div class="text-center my-2" style="line-height: 0;">
      <img src="/assets/blogs/insect_detection/motion_detection/background_image.png" 
           class="img-fluid rounded z-depth-1" 
           style="transform: rotate(180deg); display: block; margin: 20 auto;" 
           alt="Background Image">
      <div class="caption text-center" style="margin-top: 20px; font-size: 0.9rem;">
        Fig. 2: Background model for our video sequence.
      </div>
    </div>
  </li>

  <li>
    <strong>Frame difference</strong><br>
    <ul style="margin-top: 0.5rem; margin-bottom: 0;">
      <li>Subtract the background model from the current frame to get a difference image.</li>
      <li>Large pixel differences usually mean motion.</li>
      <li>Threshold the difference image into a black-and-white motion mask (white = moving pixels; black = background).</li>
    </ul>
  </li>
</ol>

<div class="col-sm mt-3 mt-md-0 text-center">
  <img src="/assets/blogs/insect_detection/motion_detection/motion_detection_mask.png" 
       class="img-fluid rounded" 
       style="margin-bottom: 20px;" 
       alt="Motion Detection Mask">
</div>
<div class="caption mt-2 text-center">
  Fig. 3: Difference mask obtained by subtracting the current frame from the background and then thresholding.
</div>

Motion detection is all around us. Here are a few real-world examples:

<ul style="margin-top: 0.5rem; margin-bottom: 0;">
  <li>Security cameras & intrusion alarms</li>
  <li>Sports highlights</li>
  <li>Wildlife monitoring (trail cams)</li>
  <li>Traffic flow analysis</li>
</ul>

---

## Insect detection with YOLO

Motion detection points out _where_ to look, and **YOLO** tells us _what_ is moving. YOLO is an object detection model that draws boxes around objects and labels them. We use YOLO for insects because:

* **Real-time:** Runs at video speed, even on small devices.  
* **All-in-one:** Finds both location and the insect’s identity in a single pass.  
* **Open-source:** Free models (YOLOv8) and easy training tools are available.

### The quick YOLO tour

<ol>
  <li>
    <strong>Candidate frames</strong><br>
    <em>After motion detection, we extract snapshots that might contain insects.</em>
    <figure class="text-center">
      <img src="/assets/blogs/insect_detection/yolo_steps/input_image.jpg" 
           alt="Input Image" 
           class="img-fluid rounded">
      <figcaption class="mt-2" style="font-size: 0.9rem; color: #555;">
        Fig. 4: Input image for insect detection, obtained from motion detection.
      </figcaption>
    </figure>
  </li>

  <li>
    <strong>Resize & grid</strong><br>
    <em>Resize each snapshot to 448×448 pixels and overlay a 7×7 grid.</em>
    <figure class="text-center">
      <img src="/assets/blogs/insect_detection/yolo_steps/cropped_grid_image.png" 
           alt="Cropped and 7x7 grid overlayed image" 
           class="img-fluid rounded">
      <figcaption class="mt-2" style="font-size: 0.9rem; color: #555;">
        Fig. 5: A 7×7 grid overlaid on the cropped image.
      </figcaption>
    </figure>
  </li>

  <li>
    <strong>One glance, many predictions</strong><br>
    <em>For each grid cell, YOLO’s neural network predicts several bounding boxes, confidence scores, and class probabilities for different insects.</em>
    <figure class="text-center">
      <img src="/assets/blogs/insect_detection/yolo_steps/grid_cell_prediction.png" 
           alt="YOLO grid cell predictions" 
           class="img-fluid rounded">
      <figcaption class="mt-2" style="font-size: 0.9rem; color: #555;">
        Fig. 6: The green box has a high confidence score and class probability; the red boxes are low confidence.
      </figcaption>
    </figure>
  </li>

  <li>
    <strong>Keep the best</strong><br>
    <em>Non-Maximum Suppression (NMS)<d-cite key="hosang2017learning"></d-cite> keeps the highest-scoring box and removes overlapping, lower-scoring ones.</em>
    <figure class="text-center">
      <img src="/assets/blogs/insect_detection/yolo_steps/non_maximum_suppression.png" 
           alt="Non Maximum Suppression process" 
           class="img-fluid rounded">
      <figcaption class="mt-2" style="font-size: 0.9rem; color: #555;">
        Fig. 7: NMS removes duplicate boxes, leaving one clear box per object.
      </figcaption>
    </figure>
    <p class="mt-2">
      After predicting many boxes, NMS:
    </p>
    <ul style="margin-top: 0.5rem; margin-bottom: 0;">
      <li>Keeps the box with the highest confidence score.</li>
      <li>Removes boxes that overlap too much (measured by Intersection over Union, or IoU).</li>
    </ul>
    <p>
      This leaves one clean box per insect. In our diagram, the green box remains and the yellow ones are discarded.
    </p>
  </li>

  <li>
    <strong>Final output</strong><br>
    <em>We get the insect’s class, a confidence score, and the bounding box coordinates.</em>
  </li>
</ol>

<p>You might be wondering:</p>

<ol>
  <li>
    <strong>How are the bounding boxes represented?</strong>
    <figure class="text-center">
      <img src="/assets/blogs/insect_detection/yolo_steps/bounding_box_representation.png" 
           alt="Bounding box representation" 
           class="img-fluid rounded">
      <figcaption class="mt-2" style="font-size: 0.9rem; color: #555;">
        Fig. 8: Bounding box representation.
      </figcaption>
    </figure>
    <ul style="margin-top: 0.5rem; margin-bottom: 0;">
      <li>Each box is defined by (cx, cy, w, h).</li>
      <li>(cx, cy) is the box center, normalized within its grid cell.</li>
      <li>(w, h) is the width and height, relative to the full image.</li>
    </ul>
  </li>

  <li>
    <strong>What if the insect overlaps two grid cells?</strong>
    <figure class="text-center">
      <img src="/assets/blogs/insect_detection/yolo_steps/overlapping_grid_cells.png" 
           alt="Overlapping grid cells" 
           class="img-fluid rounded">
      <figcaption class="mt-2" style="font-size: 0.9rem; color: #555;">
        Fig. 9: Handling overlapping grid cells.
      </figcaption>
    </figure>
    <ul style="margin-top: 10px;">
      <li>Only the cell (marked as 1) containing the insect’s center (marked by a star) makes the prediction.</li>
      <li>Neighboring cells ignore this insect and focus on objects whose centers lie inside them.</li>
    </ul>
  </li>
</ol>

---

## Conclusion & next steps

Combining **motion detection** with **YOLO** creates a nimble tag-team. On a 90,000-frame video, motion detection trimmed the candidates down to just 1,000 frames. This shows why pairing motion and object detection is essential for bio-monitoring systems that run on tight compute and energy budgets.

Next on our roadmap:

* **See even smaller bugs** — add a zoom lens or train YOLO with clearer close-ups.  
* **Dashboards for farmers** — stream live counts to a phone app for same-day action.  

Have ideas, questions, or cool bug clips? Drop a comment below — we’d love to chat! 🪲👋
