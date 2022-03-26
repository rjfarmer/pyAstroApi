# SPDX-License-Identifier: BSD-3-Clause


class AdsApiError(Exception):
    pass


class MalformedRequest(AdsApiError):
    pass


class ResourceNotFound(AdsApiError):
    pass


class ServerTooBusy(AdsApiError):
    pass


class SeverError(AdsApiError):
    pass


class QIDNotFound(AdsApiError):
    pass


class InsufficentPermisions(AdsApiError):
    pass


class LibraryAllreadyExists(AdsApiError):
    pass


class LibraryDoesNotExist(AdsApiError):
    pass


class NoADSAccount(AdsApiError):
    pass


class MetricsBlewUp(AdsApiError):
    pass


class UnableToGetResults(AdsApiError):
    pass


class AuthictationFailed(AdsApiError):
    pass


class ClassicNoCookie(AdsApiError):
    pass


class ClassicTimeOut(AdsApiError):
    pass


class NoRecordsFound(AdsApiError):
    pass


class UserDoesNotExist(AdsApiError):
    pass
