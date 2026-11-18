from pygments.style import Style
# from pygments.styles.colorful import ColorfulStyle
from pygments.token import Keyword, String, Operator, Name, Comment


class RosiAgdaStyle(Style):
  """Custom Pygments style adapting 'colorful' toward Agda-like colors."""

  name = 'rosi-agda'

  # Start from ColorfulStyle.styles and override specific tokens
  styles = {
      # Reserved Rosi keywords -> Agda-style orange
      Keyword.Reserved: 'nobold #cf6800',
      Keyword.Constants: 'bold',
      # Keyword: 'bold #cf6800',

      # Capitalized Type names -> Agda-style blue
      Keyword.Type: 'nobold #170ccd',

      # Labels -> Agda-style green
      Keyword.Label: 'nobold #008b00',
  }
