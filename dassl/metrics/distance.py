"""
Source: https://github.com/KaiyangZhou/deep-person-reid
"""
import torch
from torch.nn import functional as F


def compute_distance_matrix(input1, input2, metric="euclidean"):
    """A wrapper function for computing distance matrix.

    Each input matrix has the shape (n_data, feature_dim).

    Args:
        input1 (torch.Tensor): 2-D feature matrix.
        input2 (torch.Tensor): 2-D feature matrix.
        metric (str, optional): "euclidean" or "cosine".
            Default is "euclidean".

    Returns:
        torch.Tensor: distance matrix.
    """
    # check input
    assert isinstance(input1, torch.Tensor)
    assert isinstance(input2, torch.Tensor)
    assert input1.dim() == 2, "Expected 2-D tensor, but got {}-D".format(
        input1.dim()
    )
    assert input2.dim() == 2, "Expected 2-D tensor, but got {}-D".format(
        input2.dim()
    )
    assert input1.size(1) == input2.size(1)

    if metric == "euclidean":
        distmat = euclidean_squared_distance(input1, input2)
    elif metric == "cosine":
        distmat = cosine_distance(input1, input2)
    else:
        raise ValueError(
            "Unknown distance metric: {}. "
            'Please choose either "euclidean" or "cosine"'.format(metric)
        )

    return distmat


def euclidean_squared_distance(input1, input2):
    """Computes euclidean squared distance.

    Args:
        input1 (torch.Tensor): 2-D feature matrix.
        input2 (torch.Tensor): 2-D feature matrix.

    Returns:
        torch.Tensor: distance matrix.
    """
    m, n = input1.size(0), input2.size(0)
    mat1 = torch.pow(input1, 2).sum(dim=1, keepdim=True).expand(m, n)
    mat2 = torch.pow(input2, 2).sum(dim=1, keepdim=True).expand(n, m).t()
    distmat = mat1 + mat2
    distmat.addmm_(1, -2, input1, input2.t())
    return distmat


def cosine_distance(input1, input2):
    """Computes cosine distance.

    Args:
        input1 (torch.Tensor): 2-D feature matrix.
        input2 (torch.Tensor): 2-D feature matrix.

    Returns:
        torch.Tensor: distance matrix.
    """
    input1_normed = F.normalize(input1, p=2, dim=1)
    input2_normed = F.normalize(input2, p=2, dim=1)
    distmat = 1 - torch.mm(input1_normed, input2_normed.t())
    return distmat