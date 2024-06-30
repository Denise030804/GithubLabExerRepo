import unittest
from unittest.mock import patch, MagicMock
import oxo_cmd #rename "oxo-cmd" to "oxo_cmd"
import oxo_ui
import oxo_logic

class TestOxoCmd(unittest.TestCase):

    @patch('oxo_logic.newGame')
    @patch('oxo_ui.playGame')
    def test_do_new(self, mock_playGame, mock_newGame):
        mock_newGame.return_value = 'new_game_state'
        cmd_instance = oxo_cmd.Oxo_cmd()
        cmd_instance.do_new('')
        mock_newGame.assert_called_once()
        mock_playGame.assert_called_once_with('new_game_state')
        
    @patch('oxo_logic.restoreGame')
    @patch('oxo_ui.playGame')
    def test_do_resume(self, mock_playGame, mock_restoreGame):
        mock_restoreGame.return_value = 'saved_game_state'
        cmd_instance = oxo_cmd.Oxo_cmd()
        cmd_instance.do_resume('')
        mock_restoreGame.assert_called_once()
        mock_playGame.assert_called_once_with('saved_game_state')
        
    def test_do_quit(self):
        cmd_instance = oxo_cmd.Oxo_cmd()
        with self.assertRaises(SystemExit):
            cmd_instance.do_quit('')
        with patch('sys.stdout', new_callable=unittest.mock.Mock()) as mock_stdout:
            with self.assertRaises(SystemExit):
                cmd_instance.do_quit('')
            mock_stdout.write.assert_any_call("Goodbye...\n")

class TestOxoUi(unittest.TestCase):

    @patch('oxo_ui.oxo_logic.newGame')
    def test_startGame(self, mock_newGame):
        mock_newGame.return_value = 'new_game_state'
        result = oxo_ui.startGame()
        mock_newGame.assert_called_once()
        self.assertEqual(result, 'new_game_state')

    @patch('oxo_ui.oxo_logic.restoreGame')
    def test_resumeGame(self, mock_restoreGame):
        mock_restoreGame.return_value = 'saved_game_state'
        result = oxo_ui.resumeGame()
        mock_restoreGame.assert_called_once()
        self.assertEqual(result, 'saved_game_state')

    @patch('oxo_ui.quit')
    def test_executeChoice_quit(self, mock_quit):
        oxo_ui.executeChoice(4)
        mock_quit.assert_called_once()

    @patch('oxo_ui.startGame')
    @patch('oxo_ui.playGame')
    def test_executeChoice_start(self, mock_playGame, mock_startGame):
        mock_startGame.return_value = 'new_game_state'
        oxo_ui.executeChoice(1)
        mock_startGame.assert_called_once()
        mock_playGame.assert_called_once_with('new_game_state')

class TestOxoLogic(unittest.TestCase):

    @patch('oxo_logic.oxo_data.saveGame')
    def test_saveGame(self, mock_saveGame):
        game_state = ['X', 'O', ' ', ' ', 'X', 'O', ' ', ' ', 'X']
        oxo_logic.saveGame(game_state)
        mock_saveGame.assert_called_once_with(game_state)

    @patch('oxo_logic.oxo_data.restoreGame')
    def test_restoreGame(self, mock_restoreGame):
        mock_restoreGame.return_value = ['X', 'O', ' ', ' ', 'X', 'O', ' ', ' ', 'X']
        result = oxo_logic.restoreGame()
        mock_restoreGame.assert_called_once()
        self.assertEqual(result, ['X', 'O', ' ', ' ', 'X', 'O', ' ', ' ', 'X'])

    def test_newGame(self):
        result = oxo_logic.newGame()
        self.assertEqual(result, [' '] * 9)

    def test_userMove_valid(self):
        game = [' '] * 9
        result = oxo_logic.userMove(game, 0)
        self.assertEqual(game[0], 'X')
        self.assertEqual(result, "")

    def test_userMove_invalid(self):
        game = ['X'] * 9
        with self.assertRaises(ValueError):
            oxo_logic.userMove(game, 0)

    @patch('random.choice')
    def test_computerMove(self, mock_choice):
        game = [' '] * 9
        mock_choice.return_value = 0
        result = oxo_logic.computerMove(game)
        self.assertEqual(game[0], 'O')
        self.assertEqual(result, "")

    @patch('random.choice')
    def test_computerMove_draw(self, mock_choice):
        game = ['X', 'X', 'O', 'O', 'O', 'X', 'X', 'O', 'X']
        result = oxo_logic.computerMove(game)
        self.assertEqual(result, 'D')

if __name__ == '__main__':
    unittest.main()
