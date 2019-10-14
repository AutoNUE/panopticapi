# AutoNUE 2019 Panoptic Segmentation Task API 
This is adapted from [COCO 2018 Panoptic Segmentation Task API](http://cocodataset.org/#panoptic-2018).

To install panopticapi, run:
```
pip install git+https://github.com/AutoNUE/panopticapi.git
```

## Summary
**Evaluation script**

[panopticapi/evaluation.py](panopticapi/evaluation.py) calculates [PQ metrics](http://cocodataset.org/#panoptic-eval).
For more information about the script usage: `python -m panopticapi.evaluation --help`
