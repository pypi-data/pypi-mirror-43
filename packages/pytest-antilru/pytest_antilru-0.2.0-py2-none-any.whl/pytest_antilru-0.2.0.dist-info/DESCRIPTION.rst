Caching with functools.lru_cache is great for performance. It works so well that it'll even
speed up your unit test runs. All you need to sacrifice in return is test isolation and your sanity.

Imagine, you mock some things out and a function caches those results. On your next test run, it doesn't matter what you
mock, the results are already cached. Now trying running those two test out-of-order sequence and tell me how it goes.


