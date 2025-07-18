# flake8: noqa: E501
import unittest
from unittest.mock import patch
import update_extensions


class TestRefGeneration(unittest.TestCase):
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

        self.maxDiff = None
        self.assertEqual(
            generator.extensions_data,
            expected_data,
        )


if __name__ == "__main__":
    unittest.main()
