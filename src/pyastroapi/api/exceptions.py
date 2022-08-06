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


class InsufficientPermissions(AdsApiError):
    pass


class LibraryAlreadyExists(AdsApiError):
    pass


class LibraryDoesNotExist(AdsApiError):
    pass


class NoADSAccount(AdsApiError):
    pass


class MetricsBlewUp(AdsApiError):
    pass


class UnableToGetResults(AdsApiError):
    pass


class AuthenticationFailed(AdsApiError):
    pass


class ClassicNoCookie(AdsApiError):
    pass


class ClassicTimeOut(AdsApiError):
    pass


class ClassicUserDidNotMakeAccount(AdsApiError):
    pass


class NoRecordsFound(AdsApiError):
    pass


class UserDoesNotExist(AdsApiError):
    pass
