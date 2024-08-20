from unittest import TestCase

from typing import cast

import pygame
from pygame.rect import Rect

from ui import Theme
from ui.component.text import TextRenderer, TextTokenizer
from ui.component.text.token import ContentTextToken, ReturnTextToken, IconTextToken, TextStyle

from test.misc import compareSurfaces


class TestWorld(TestCase):

    def test_tokenizer(self):
        theme = Theme()
        tokenizer = TextTokenizer(theme)
        style = TextStyle("default")
        tokens = tokenizer.parse(f"Resources<br><food> 100 ", style)

        self.assertEqual(len(tokens), 4)

        self.assertIsInstance(tokens[0], ContentTextToken)
        self.assertEqual(cast(ContentTextToken, tokens[0]).content, "Resources")

        self.assertIsInstance(tokens[1], ReturnTextToken)

        self.assertIsInstance(tokens[2], IconTextToken)
        self.assertEqual(cast(IconTextToken, tokens[2]).tile, Rect(0, 20, 5, 5))

        self.assertIsInstance(tokens[3], ContentTextToken)
        self.assertEqual(cast(ContentTextToken, tokens[3]).content, " 100 ")

    def test_renderer(self):
        theme = Theme()
        renderer = TextRenderer(theme, "default")
        surface = renderer.render(
            "Test<br>"
            "<i>Italic</i><br>"
            "<b>Bold</b><br>"
            "<u>Underline</u><br>"
            "<i><b><u>All</u></b></i><br>"
            '<s color="warning">Color</s><br>'
            'Icon:<elder>'
        )
        if False:  # Update test data
            pygame.image.save(surface, "test/data/text_renderer.png")
        #pygame.image.save(surface, "test.png")
        check = pygame.image.load("test/data/text_renderer.png")
        self.assertTrue(compareSurfaces(surface, check))

