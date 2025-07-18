# PRIMARY OBJECTIVE: AUTOMATE `spec-extended.json` and `spec-extended.min.json`

**Your primary goal is to build and maintain a script that automatically generates the `extensions.ref.json` then `extensions.json` and `extensions.min.json` files by running the script through Github's Action Workflow (free plan) on a weekly basis.**

This script must scrape all relevant official and community sources for non-spec information about the Telegram Bot API. The scraped data, including source URLs and highlighted text, should first be stored in a reference file named `extensions.ref.json`. This file will then be used to generate `extensions.json` and `extensions.min.json`.

Direct manual creation or updating of `extensions.json` is **not** the objective; the focus is on the automation script.

Incorporate a lightweight AI component to enhance the script's ability to recognize relevant information and suggest optimal data structures (aligned with api.json for easy merging), while staying within the constraints of the free GitHub Actions plan.

---

You are contributing to a public GitHub repository called telegram-bot-api-spec-extended:
https://github.com/Sherbeeny/telegram-bot-api-spec-extended

This repo automatically pulls the official Telegram Bot API spec JSON (api.json & api.min.json) from PaulSonOfLars/telegram-bot-api-spec every day.

Implement a script that builds and maintains a complementary JSON file, named extensions.ref.json, which contain everything that the base spec files don’t include, but is essential for real-world mocking, testing, tooling, and understanding of Telegram Bot API behaviors. Each info must include a "ref" key of the source of that info (anchored & text highlighted).

The ref extension file will later be used to generate extensions.json and extensions.min.json.. and then be merged with the spec files to create spec-extended.json & spec-extended.min.json

✅ The script must format all extra data as valid OpenAPI extensions using the x- prefix (e.g., x-rate-limit, x-premium-access, x-premium-broadcast, etc.) to ensure that the final spec-extended.json will be a valid OpenAPI-compatible file.

✅ The extensions file must be a clean object mirroring the Telegram API structure and methods (api.json) in addition to the extra info and behaviours that's not found in the spec file, e.g.:

{
  "sendMessage": {
    "x-rate-limit": { "per_chat": 1, "per_second": 30 },
    "x-premium-restrictions": { "max_message_length": 4096 }
  },
  "forwardMessage": {
    "x-rate-limit": { "per_chat": 10, "global_per_minute": 300 }
  }
}

🧠 The script to be **weekly** run by a github action workflow to:
	•	Scrape data from https://core.telegram.org/bots/api, https://core.telegram.org/bots/faq, and https://core.telegram.org/bots/features
	•	Use known community knowledge, experiments, or test cases to deduce unofficial limits and behaviors
	•	Include documentation-specific fields like x-notes, x-simulated-behavior, x-likely-side-effects, etc.
behaviors
	•	Incorporate a lightweight AI component to enhance recognizing which info should be added to extensions.ref.json and the best structure/names to use for the keys/maps of that file as a supplement to api.json without repeating info already included in api.json because the two files will next be merged into spec-extended.json (considering that this script will run weekly on the free plan of GitHub)
	•	The json files must also contain a “x-last-check” and “x-last-edit” timestamps, actual Cairo timezone as well, "x-last-check" is always updated with each script run. but "x-last-edit" is only updated when the new json file has different info from the previous json files (ignoring "x-last-check" value).
	•	If all scraped data is unchanged, it must be guaranteed that the script, with AI, will produce the same exact json file. (except for the new timestamp value of "x-last-check"). This is not only about cases where telegram changes a numeric value in a ref page, but I’m also about when Telegram announcing changes through a punch of new text (new sentence, new paragraph, FAQ question, new article… etc) which should only result in updating a value in the json file instead of adding a new key-value pair. Only add new key-value pair when it's certain it's necessary as a new set of info that can't be updated to an existing key-value pair. It’s critical to maintain the same structure and key names across file versions. 

🛑 The script should not generate data that is already present in api.json. Only augment or extend it with additional context, behaviors, and rules that Telegram does not officially define in their OpenAPI spec.

📁 The final output of the weekly script must:
	•   First create/update the file “extensions.ref.json” which contains a reference url of the source of the info/behavior (anchor & text highlighted), name the key “ref”. 
	•	Then the script would generate “extensions.json” & “extensions.min.json” from the “extensions.ref.json”.
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
