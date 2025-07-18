import unittest
from unittest.mock import patch
import update_extensions


class TestGenerator(unittest.TestCase):
    @patch("update_extensions.scraper.scrape_all")
    def test_generate_extensions_data_from_ref(self, mock_scrape_all):
        mock_scrape_all.return_value = {
            "x-rate-limit": {
                "per_chat_per_second": {
                    "value": 1,
                    "ref": {
                        "url": "https://core.telegram.org/bots/faq#my-bot-is-hitting-limits-how-do-i-avoid-this",
                        "text": "In a single chat, avoid sending more than one message per second. We may allow short bursts that go over this limit, but eventually you'll begin receiving 429 errors.",
                    },
                },
                "group_per_minute": {
                    "value": 20,
                    "ref": {
                        "url": "https://core.telegram.org/bots/faq#my-bot-is-hitting-limits-how-do-i-avoid-this",
                        "text": "In a group, bots are not be able to send more than 20 messages per minute.",
                    },
                },
                "broadcast_per_second": {
                    "value": 30,
                    "ref": {
                        "url": "https://core.telegram.org/bots/faq#my-bot-is-hitting-limits-how-do-i-avoid-this",
                        "text": "For bulk notifications, bots are not able to broadcast more than about 30 messages per second, unless they enable paid broadcasts to increase the limit.",
                    },
                },
            },
            "x-file-size-limits": {
                "upload_mb": {
                    "value": 50,
                    "ref": {
                        "url": "https://core.telegram.org/bots/faq#how-do-i-upload-a-large-file",
                        "text": "Bots can currently send files of any type of up to 50 MB in size, so yes, very large files won't work for now. Sorry. This limit may be changed in the future.",
                    },
                },
                "download_mb": {
                    "value": 20,
                    "ref": {
                        "url": "https://core.telegram.org/bots/faq#how-do-i-download-files",
                        "text": "Use the getFile method. Please note that this will only work with files of up to 20 MB in size.",
                    },
                },
            },
        }

        generator = update_extensions.Generator()
        generator.extensions_ref_data = mock_scrape_all.return_value
        generator.generate_extensions_data_from_ref()

        expected_data = {
            "sendMessage": {
                "x-rate-limit": {
                    "per_chat_per_second": {
                        "value": 1,
                        "ref": {
                            "url": "https://core.telegram.org/bots/faq#my-bot-is-hitting-limits-how-do-i-avoid-this",
                            "text": "In a single chat, avoid sending more than one message per second. We may allow short bursts that go over this limit, but eventually you'll begin receiving 429 errors.",
                        },
                    },
                    "group_per_minute": {
                        "value": 20,
                        "ref": {
                            "url": "https://core.telegram.org/bots/faq#my-bot-is-hitting-limits-how-do-i-avoid-this",
                            "text": "In a group, bots are not be able to send more than 20 messages per minute.",
                        },
                    },
                    "broadcast_per_second": {
                        "value": 30,
                        "ref": {
                            "url": "https://core.telegram.org/bots/faq#my-bot-is-hitting-limits-how-do-i-avoid-this",
                            "text": "For bulk notifications, bots are not able to broadcast more than about 30 messages per second, unless they enable paid broadcasts to increase the limit.",
                        },
                    },
                },
                "x-restrictions": {"text": {"max_length": 4096}},
            },
            "sendPhoto": {
                "x-rate-limit": {
                    "per_chat_per_second": {
                        "value": 1,
                        "ref": {
                            "url": "https://core.telegram.org/bots/faq#my-bot-is-hitting-limits-how-do-i-avoid-this",
                            "text": "In a single chat, avoid sending more than one message per second. We may allow short bursts that go over this limit, but eventually you'll begin receiving 429 errors.",
                        },
                    },
                    "group_per_minute": {
                        "value": 20,
                        "ref": {
                            "url": "https://core.telegram.org/bots/faq#my-bot-is-hitting-limits-how-do-i-avoid-this",
                            "text": "In a group, bots are not be able to send more than 20 messages per minute.",
                        },
                    },
                    "broadcast_per_second": {
                        "value": 30,
                        "ref": {
                            "url": "https://core.telegram.org/bots/faq#my-bot-is-hitting-limits-how-do-i-avoid-this",
                            "text": "For bulk notifications, bots are not able to broadcast more than about 30 messages per second, unless they enable paid broadcasts to increase the limit.",
                        },
                    },
                },
                "x-restrictions": {
                    "photo": {
                        "max_size_mb": 10,
                        "max_dimensions_total": 10000,
                        "max_ratio": 20,
                    },
                    "caption": {"max_length": 1024},
                },
            },
            "editMessageText": {
                "x-rate-limit": {
                    "per_chat_per_second": {
                        "value": 1,
                        "ref": {
                            "url": "https://core.telegram.org/bots/faq#my-bot-is-hitting-limits-how-do-i-avoid-this",
                            "text": "In a single chat, avoid sending more than one message per second. We may allow short bursts that go over this limit, but eventually you'll begin receiving 429 errors.",
                        },
                    },
                    "group_per_minute": {
                        "value": 20,
                        "ref": {
                            "url": "https://core.telegram.org/bots/faq#my-bot-is-hitting-limits-how-do-i-avoid-this",
                            "text": "In a group, bots are not be able to send more than 20 messages per minute.",
                        },
                    },
                    "broadcast_per_second": {
                        "value": 30,
                        "ref": {
                            "url": "https://core.telegram.org/bots/faq#my-bot-is-hitting-limits-how-do-i-avoid-this",
                            "text": "For bulk notifications, bots are not able to broadcast more than about 30 messages per second, unless they enable paid broadcasts to increase the limit.",
                        },
                    },
                },
                "x-restrictions": {
                    "edit": {"max_age_hours": 48},
                    "text": {"max_length": 4096},
                },
            },
            "answerCallbackQuery": {
                "x-rate-limit": {
                    "per_chat_per_second": {
                        "value": 1,
                        "ref": {
                            "url": "https://core.telegram.org/bots/faq#my-bot-is-hitting-limits-how-do-i-avoid-this",
                            "text": "In a single chat, avoid sending more than one message per second. We may allow short bursts that go over this limit, but eventually you'll begin receiving 429 errors.",
                        },
                    },
                    "group_per_minute": {
                        "value": 20,
                        "ref": {
                            "url": "https://core.telegram.org/bots/faq#my-bot-is-hitting-limits-how-do-i-avoid-this",
                            "text": "In a group, bots are not be able to send more than 20 messages per minute.",
                        },
                    },
                    "broadcast_per_second": {
                        "value": 30,
                        "ref": {
                            "url": "https://core.telegram.org/bots/faq#my-bot-is-hitting-limits-how-do-i-avoid-this",
                            "text": "For bulk notifications, bots are not able to broadcast more than about 30 messages per second, unless they enable paid broadcasts to increase the limit.",
                        },
                    },
                },
                "x-restrictions": {"text": {"max_length": 200}},
            },
            "getUpdates": {
                "x-rate-limit": {
                    "per_chat_per_second": {
                        "value": 1,
                        "ref": {
                            "url": "https://core.telegram.org/bots/faq#my-bot-is-hitting-limits-how-do-i-avoid-this",
                            "text": "In a single chat, avoid sending more than one message per second. We may allow short bursts that go over this limit, but eventually you'll begin receiving 429 errors.",
                        },
                    },
                    "group_per_minute": {
                        "value": 20,
                        "ref": {
                            "url": "https://core.telegram.org/bots/faq#my-bot-is-hitting-limits-how-do-i-avoid-this",
                            "text": "In a group, bots are not be able to send more than 20 messages per minute.",
                        },
                    },
                    "broadcast_per_second": {
                        "value": 30,
                        "ref": {
                            "url": "https://core.telegram.org/bots/faq#my-bot-is-hitting-limits-how-do-i-avoid-this",
                            "text": "For bulk notifications, bots are not able to broadcast more than about 30 messages per second, unless they enable paid broadcasts to increase the limit.",
                        },
                    },
                },
                "x-restrictions": {
                    "limit": {
                        "min_value": 1,
                        "max_value": 100,
                        "default_value": 100,
                    },
                    "timeout": {"default_value": 0},
                },
            },
        }

        self.assertEqual(
            generator.extensions_data,
            expected_data,
        )

    @patch("update_extensions.scraper.scrape_all")
    @patch("update_extensions.AIComponent")
    def test_ai_component_is_called(self, mock_ai_component, mock_scrape_all):
        mock_scrape_all.return_value = {"methods": {}, "types": {}}
        update_extensions.main()
        mock_ai_component.assert_called_once_with({"methods": {}, "types": {}})
        mock_ai_component.return_value.analyze_data.assert_called_once()

    def test_analyze_data(self):
        extensions_ref_data = {
            "methods": {"getMe": {"description": "A simple method"}},
            "types": {"User": {"description": "A Telegram user"}},
        }
        ai_component = update_extensions.AIComponent(extensions_ref_data)
        with patch("builtins.print") as mock_print:
            ai_component.analyze_data()
            mock_print.assert_any_call("Most common words:")
            mock_print.assert_any_call("- simple: 1")
            mock_print.assert_any_call("- method: 1")
            mock_print.assert_any_call("- telegram: 1")
            mock_print.assert_any_call("- user: 1")


if __name__ == "__main__":
    unittest.main()
