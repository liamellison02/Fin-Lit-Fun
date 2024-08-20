import unittest
import pygame

pygame.init()
pygame.display.set_mode((1024, 768))

loader = unittest.TestLoader()
tests = loader.discover('test')
testRunner = unittest.runner.TextTestRunner()
testRunner.run(tests)

pygame.quit()
