# py-hcaptcha
 
Library for creating and interacting with hCaptcha challenges.

This project relies on my [xrequests](https://github.com/h0nde/xrequests) library which is also not available on pip.

# Installation
```bash
pip install -U git+https://github.com/h0nde/xrequests
pip install -U git+https://github.com/h0nde/py-hcaptcha
```

# Solving
Redis is required for solving, you can download and install it [here](https://redislabs.com/blog/redis-on-windows-10/).

An example script for solving is available at [auto_solve.py](https://github.com/h0nde/py-hcaptcha/blob/main/examples/auto_solve.py).

# Docs

## Solvers
### Solver(database=None, collect_data=True, min_answers=1, max_tasks=0, debug=False)
`database`: `redis.Redis` instance.
`collect_data`: Will attempt to collect new data if enabled.
`min_answers`: Minimum number of answers for a challenge. Will fill blanks spots with random guesses.
`max_tasks`: Maximum number of answers for a challenge. Will skip challenges that are above set amount.
`debug`:

### Solver.get_token(sitekey, page_url, http_client2=None, **challenge_kwargs)
Creates challenge based on parameters and attempts to solve it. Returns token if valid.

## Challenges
### Challenge(sitekey, page_url, invisible=None, widget_id=None, version=None, agent=None, http_client=None)
Creates hCaptcha challenge for provided `sitekey`. Parameter `http_client` can be a `requests.Session` or `xrequests.Session` object.

### Challenge.key
Challenge identifier key.

### Challenge.type
Type of challenge:
- `image_label_binary` (select image tile)

### Challenge.question
Question of the challenge (english).

### Challenge.tasks
List of `Task` objects for the challenge.

### Challenge.token
The solution token to be submitted to your website of choice.

### Challenge.solve(answers)
Takes in list of `Task` objects or task keys.
Returns solution token if valid.

## Tasks
Tasks represent each clickable image on your challenge. Task objects can be passed as a list to `Challenge.solve`

### Task.key
Identifier for the task.

### Task.url
URL for task image.

### Task.content()
Downloads and returns raw image content (bytes).

### Task.image()
Downloads image content and returns a `PIL.Image.Image` object.

### Task.phash(size=16)
Downloads task image and returns calculated phash using provided size.

## Agents
`Agent` objects contain information about the "simulated" browser and device, such as the user agent, screen resolution, logical processors, etc,.

## Exceptions

### HCaptchaError
Base class for all other exceptions.

### ApiError
Raised when server returns false for either `pass` or `success` parameters in response, or status code 429.
