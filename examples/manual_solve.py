import hcaptcha

ch = hcaptcha.Challenge(
    sitekey="13257c82-e129-4f09-a733-2a7cb3102832",
    page_url="https://dashboard.hcaptcha.com/signup"
)

answers = []
for task in ch.tasks:
    task.image().show()
    if input("Enter any key to select this image: "):
        answers.append(task)
        print("Selected image!")

token = ch.solve(answers)
if token:
    print("Solved!", token)
else:
    print("Incorrect answer(s) :(")