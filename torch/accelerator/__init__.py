# mypy: allow-untyped-defs
r"""
This package introduces support for the current :ref:`accelerator<accelerators>` in python.
"""

from typing import Any

import torch

from ._utils import _device_t, _get_device_index


def current_accelerator() -> torch.device:
    r"""Return the device of the current :ref:`accelerator<accelerators>`.
    Note that the index of the returned :class:`torch.device` will be ``None``, use
    use :func:`torch.accelerator.current_device_idx` to know the current index being used.

    Returns:
        torch.device: return the current accelerator as :class:`torch.device`.
            If no available accelerators, return cpu device.

    Example::

        >>> # xdoctest: +SKIP
        >>> if torch.accelerator.current_accelerator().type == 'cuda':
        >>>     is_half_supported = torch.cuda.has_half()
        >>> elif torch.accelerator.current_accelerator().type == 'xpu':
        >>>     is_half_supported = torch.xpu.get_device_properties().has_fp16
    """
    return torch._C._accelerator_getAccelerator()


def device_count() -> int:
    r"""Return the number of current :ref:`accelerator<accelerators>` available.

    Returns:
        int: the number of the current :ref:`accelerator<accelerators>` available.
            If no available accelerators, return 0.
    """
    return torch._C._accelerator_deviceCount()


def is_available() -> bool:
    r"""Check if there is an available :ref:`accelerator<accelerators>`.

    Returns:
        bool: A boolean indicating if there is an available :ref:`accelerator<accelerators>`.

    Example::

        >>> assert torch.accelerator.is_available() "No available accelerators detected."
    """
    return device_count() > 0


def current_device_idx() -> int:
    r"""Return the index of a currently selected device for the current :ref:`accelerator<accelerators>`.

    Returns:
        int: the index of a currently selected device.
    """
    return torch._C._accelerator_getDeviceIndex()


def set_device_idx(device: _device_t, /) -> None:
    r"""Set the current device index to a given device.

    Args:
        device (:class:`torch.device`, str, int): a given device that must match the current
            :ref:`accelerator<accelerators>` device type. This function is a no-op if this device index is negative.
    """
    device_index = _get_device_index(device)
    torch._C._accelerator_setDeviceIndex(device_index)


def current_stream(device: _device_t = None, /) -> torch.Stream:
    r"""Return the currently selected stream for a given device.

    Args:
        device (:class:`torch.device`, str, int, optional): a given device that must match the current
            :ref:`accelerator<accelerators>` device type. If not given,
            use :func:`torch.accelerator.current_device_idx` by default.
    Returns:
        torch.Stream: the currently selected stream for a given device.
    """
    device_index = _get_device_index(device, True)
    return torch._C._accelerator_getStream(device_index)


def set_stream(stream: torch.Stream) -> None:
    r"""Set the current stream to a given stream.

    Args:
        stream (torch.Stream): a given stream that must match the current :ref:`accelerator<accelerators>` device type.
            This function will set the current device to the device of the given stream.
    """
    torch._C._accelerator_setStream(stream)


def synchronize(device: _device_t = None, /) -> None:
    r"""Wait for all kernels in all streams on the given device to complete.

    Args:
        device (:class:`torch.device`, str, int, optional): device for which to synchronize. It must match
            the current :ref:`accelerator<accelerators>` device type. If not given,
            use :func:`torch.accelerator.current_device_idx` by default.

    Example::

        >>> # xdoctest: +REQUIRES(env:TORCH_DOCTEST_CUDA)
        >>> assert torch.accelerator.is_available() "No available accelerators detected."
        >>> start_event = torch.Event(enable_timing=True)
        >>> end_event = torch.Event(enable_timing=True)
        >>> start_event.record()
        >>> tensor = torch.randn(100, device=torch.accelerator.current_accelerator())
        >>> sum = torch.sum(tensor)
        >>> end_event.record()
        >>> torch.accelerator.synchronize()
        >>> elapsed_time_ms = start_event.elapsed_time(end_event)
    """
    device_index = _get_device_index(device, True)
    torch._C._accelerator_synchronizeDevice(device_index)


__all__ = [
    "current_accelerator",
    "current_device_idx",
    "current_stream",
    "device_count",
    "is_available",
    "set_device_idx",
    "set_stream",
    "synchronize",
]
