### Submission files format
You must submit the following
- JSON file containing the annotations of the results.[See `sample.json`]
- Folder containing the predicted images.[See `sample_data/`]

Format of JSON file:
JSON file must be of the format:
```
{
  "annotations": [segments_info1, segments_info2, ...],
  "categories": [category1, category2, ...]
}

```

`segment_info` objects represent the detected instances. Each object will have the following format:
```
{
  "area": ...,
  "category_id": ...,
  "iscrowd": ...,
  "id": ...,
}
```
- [**integer**] `id` is unique for each instance. IDs are encoded for each instance, see section on ID encoding.
- [**integer**] `category_id` is unique for each category of instances.
- [**integer**] `area` represents the total number of pixels in the instance.
- [**0 or 1**] `iscrowd` represent crowd segments. (Crowd segments are ignored during evaluation)

`category` objects represent the classes that need to be segmented. They have the following format:
```
{
  "supercategory": "outdoor",
  "color": [250, 0, 30],
  "isthing": 1,
  "id": 15,
  "name": "bench"
}
```
- [**string**] `supercategory`/`name` are optional strings used to denote the class or parent class of that category.
- [**integer array**] `color` is an optional argument used to denote the approximate/average color the instances of a category might have.
- [**0 or 1**] `isthing` is used to differentiate between thing/stuff categories.
- [**integer**] `id` this is the same as `category_id` in `segment_info` objects. It is unique for each category.



































.
