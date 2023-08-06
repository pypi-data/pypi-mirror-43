# storystructure package

A Python package to explore the stucture of branching stories

## Installation

```
pip install storystructure
```

## Example usage

To use the package two input data files are necessary:

- An *edgelist* file with columns `source` and `target`
- A *node attributes* file with columns `node` and `attribute`. The attribute column must be on of the following values `good`, `bad`, `pause`
