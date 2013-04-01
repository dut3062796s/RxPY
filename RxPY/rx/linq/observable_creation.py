from rx.observable import Observable
from rx.anonymousobservable import AnonymousObservable

from rx.disposables import Disposable
from rx.concurrency import ImmediateScheduler

class ObservableCreation(object):

    @classmethod
    def create(cls, subscribe):
        def _subscribe(observer):
            return Disposable.create(subscribe(observer))
        
        return AnonymousObservable(_subscribe)

    @classmethod
    def create_with_disposable(cls, subscribe):
        return cls(subscribe)

    @classmethod
    def defer(cls, observable_factory):
        def subscribe(observer):
            result = None
            try:
                result = observable_factory()
            except Exception as ex:
                return Observable.throw(ex).subscribe(observer)
            
            return result.subscribe(observer)

        return AnonymousObservable(subscribe)

    @classmethod
    def empty(cls, scheduler=None):
        scheduler = scheduler or ImmediateScheduler()
    
        def subscribe(observer):
            def action(scheduler, state):
                observer.on_completed()

            return scheduler.schedule(action)

        return AnonymousObservable(subscribe)

# var observableFromArray = Observable.fromArray = function (array, scheduler) {
#     scheduler || (scheduler = currentThreadScheduler)
#     return new AnonymousObservable(function (observer) {
#         var count = 0
#         return scheduler.scheduleRecursive(function (self) {
#             if (count < array.length) {
#                 observer.onNext(array[count++])
#                 self()
#             } else {
#                 observer.onCompleted()
#             }
#         })
#     })
# }

# Observable.generate = function (initialState, condition, iterate, resultSelector, scheduler) {
#     scheduler || (scheduler = currentThreadScheduler)
#     return new AnonymousObservable(function (observer) {
#         var first = true, state = initialState
#         return scheduler.scheduleRecursive(function (self) {
#             var hasResult, result
#             try {
#                 if (first) {
#                     first = false
#                 } else {
#                     state = iterate(state)
#                 }
#                 hasResult = condition(state)
#                 if (hasResult) {
#                     result = resultSelector(state)
#                 }
#             } catch (exception) {
#                 observer.onError(exception)
#                 return
#             }
#             if (hasResult) {
#                 observer.onNext(result)
#                 self()
#             } else {
#                 observer.onCompleted()
#             }
#         })
#     })
# }
    @classmethod
    def never(cls):
        def subscribe(observer):
            return Disposable.empty()

        return AnonymousObservable(subscribe)

# Observable.range = function (start, count, scheduler) {
#     scheduler || (scheduler = currentThreadScheduler)
#     return new AnonymousObservable(function (observer) {
#         return scheduler.scheduleRecursiveWithState(0, function (i, self) {
#             if (i < count) {
#                 observer.onNext(start + i)
#                 self(i + 1)
#             } else {
#                 observer.onCompleted()
#             }
#         })
#     })
# }

# Observable.repeat = function (value, repeatCount, scheduler) {
#     scheduler || (scheduler = currentThreadScheduler)
#     if (repeatCount == undefined) {
#         repeatCount = -1
#     }
#     return observableReturn(value, scheduler).repeat(repeatCount)
# }

# var observableReturn = Observable.returnValue = function (value, scheduler) {
#     scheduler || (scheduler = immediateScheduler)
#     return new AnonymousObservable(function (observer) {
#         return scheduler.schedule(function () {
#             observer.onNext(value)
#             observer.onCompleted()
#         })
#     })
# }

    @classmethod
    def throw_exception(cls, exception, scheduler=None):
        scheduler = scheduler or ImmediateScheduler()
        
        exception = Exception(exception) if type(exception) is Exception else exception

        def subscribe(observer):
            def action(scheduler, state):
                observer.on_error(exception)

            return scheduler.schedule(action)
        return AnonymousObservable(subscribe)

# Observable.using = function (resourceFactory, observableFactory) {
#     return new AnonymousObservable(function (observer) {
#         var disposable = disposableEmpty, resource, source
#         try {
#             resource = resourceFactory()
#             if (resource) {
#                 disposable = resource
#             }
#             source = observableFactory(resource)
#         } catch (exception) {
#             return new CompositeDisposable(observableThrow(exception).subscribe(observer), disposable)
#         }
#         return new CompositeDisposable(source.subscribe(observer), disposable)
#     })
# }                 

Observable.create = ObservableCreation.create
Observable.empty = ObservableCreation.empty
Observable.never = ObservableCreation.never
Observable.throw_exception = ObservableCreation.throw_exception