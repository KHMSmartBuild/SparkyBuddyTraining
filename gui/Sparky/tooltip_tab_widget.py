from PyQt5.QtWidgets import QTabWidget, QTabBar


class TooltipTabWidget(QTabWidget):
    """
    A QTabWidget that shows a tooltip of the tab text if it is truncated.
    """

    def __init__(self):
        super().__init__()

        # Set the custom QTabBar that can show a tooltip
        self.setTabBar(TooltipTabBar(self))
    
    # Set the custom QTabBar that can show a tooltip
    """
    Initializes the class and sets the custom QTabBar that can show a tooltip.

    Args:
        self: The object itself.

    Returns:
        None.
    """
    def setTabText(self, index, text):
        super().setTabText(index, text)

        # Update the tooltip if the text is truncated
        if self.isTabTextTruncated(index):
            self.tabBar().setTabToolTip(index, text)
        else:
            self.tabBar().setTabToolTip(index, "")


    # Update the tooltip if the text is truncated
    """
    Checks if the text on a tab at the given index is truncated and returns a boolean value.

    :param index: The index of the tab to be checked.
    :return: True if the text on the tab is truncated, False otherwise.
    """
    def isTabTextTruncated(self, index):
        tab_rect = self.tabBar().tabRect(index)
        text_rect = self.tabBar().tabRect(index).intersected(self.tabBar().textRect(index))
        return text_rect.width() < tab_rect.width()


class TooltipTabBar(QTabBar):
    """
    A QTabBar that can show a tooltip.
    """
    def __init__(self, parent):
        super().__init__(parent)


    # Set the custom QTabBar that can show a tooltip
    """
    Sets the tooltip for the given tab.
    @param index: the index of the tab to set the tooltip for
    @param text: the text to set as the tooltip
    @return: None
    """
    def setTabToolTip(self, index, text):
        super().setTabToolTip(index, text)

        # Make sure the tooltip is shown if the text is truncated
        if self.tabRect(index).width() < self.fontMetrics().boundingRect(text).width():
            self.setToolTip(text)
        else:
            self.setToolTip("")
