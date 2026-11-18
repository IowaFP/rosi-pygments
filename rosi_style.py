from pygments.style import Style
from pygments.styles.colorful import ColorfulStyle
from pygments.token import Keyword, String, Operator, Name, Comment


class RosiAgdaStyle(ColorfulStyle):
  """Custom Pygments style adapting 'colorful' toward Agda-like colors."""

  name = 'rosi-agda'

  # Start from ColorfulStyle.styles and override specific tokens
  styles = {
      **ColorfulStyle.styles,
      # Reserved Rosi keywords -> Agda-style orange
      Keyword.Reserved: 'bold #cf6800',
      # Keyword: 'bold #cf6800',

      # Capitalized Type names -> Agda-style blue
      Keyword.Type: '#170ccd',

      # Labels -> Agda-style green
      String.Other: '#008b00'
  }
