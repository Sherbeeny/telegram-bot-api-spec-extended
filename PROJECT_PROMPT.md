You are contributing to a public GitHub repository called telegram-bot-api-spec-extended:
https://github.com/Sherbeeny/telegram-bot-api-spec-extended

This repo automatically pulls the official Telegram Bot API spec JSON (api.json & api.min.json) from PaulSonOfLars/telegram-bot-api-spec every day.

I want you to now build and maintain a complementary JSON file, named extensions.json & extensions.min.json, which contain everything that the base spec files don’t include, but is essential for real-world mocking, testing, tooling, and understanding of Telegram Bot API behaviors.

the extensions files will later be merged the spec files to create spec-extended.json & spec-extended.min.json

✅ You must format all extra data as valid OpenAPI extensions using the x- prefix (e.g., x-rate-limit, x-premium-access, etc.) to ensure that the final spec-extended.json will be a valid OpenAPI-compatible file.

✅ You will write this extensions.json file as a clean object mirroring the Telegram API structure and methods, e.g.:

{
  "sendMessage": {
    "x-rate-limit": { "per_chat": 1, "per_second": 30 },
    "x-premium-restrictions": { "max_message_length": 4096 }
  },
  "forwardMessage": {
    "x-rate-limit": { "per_chat": 10, "global_per_minute": 300 }
  }
}

🧠 You will need to create a script to be daily run by a github action workflow to:
	•	Scrape data from https://core.telegram.org/bots/api, https://core.telegram.org/bots/faq, and https://core.telegram.org/bots/features
	•	Use known community knowledge, experiments, or test cases to deduce unofficial limits and behaviors
	•	Include documentation-specific fields like x-notes, x-simulated-behavior, x-likely-side-effects, etc.

🛑 You should not copy data that is already present in api.json. Only augment or extend it with additional context, behaviors, and rules that Telegram does not officially define in their OpenAPI spec.

📁 The final output of the daily script must:
	•	Be saved to extensions.json (and extensions.min.json, similar to api.json and its api.min.json)
	•	Be self-contained and structured for easy merging with api.json & api.min.json
	•	Avoid hard-coding unstable values (note any uncertainties via x-source or x-confidence)
	•	The merged versions: spec-extended.json and spec-extended.min.json


🧩 Example categories to include per method or globally:
	•	x-rate-limit (global, per-method, per-chat, per-user)
	•	x-tier-access (premium vs non-premium, verified bots)
	•	x-webhook-behavior and x-long-polling-behavior
	•	x-restrictions (e.g., max number of buttons, max size of media, max length of messages)
	•	x-errors (typical errors this method may trigger and how to simulate them)
	•	x-expected-update-sequence (how Telegram behaves when responding to this method)

🎯 The goal is to build a foundation for realistic Telegram bot simulation that:
	•	Powers mocks and test engines (like telegram-mocker)
	•	Helps lint, simulate, and test edge cases in Telegram bots
	•	Works even when Telegram’s docs are incomplete or vague

Please start by generating a first draft of extensions.json with useful x- fields for at least 5 key methods: sendMessage, sendPhoto, editMessageText, answerCallbackQuery, and getUpdates.
