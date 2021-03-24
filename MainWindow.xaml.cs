using System;
using System.Collections.Generic;
using System.IO;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.Windows;
using System.Windows.Controls;
using System.Windows.Data;
using System.Windows.Documents;
using System.Windows.Input;
using System.Windows.Media;
using System.Windows.Media.Imaging;
using System.Windows.Navigation;
using System.Windows.Shapes;
using System.Threading;
using System.Diagnostics;

namespace QBot
{
    /// <summary>
    /// Interaction logic for MainWindow.xaml
    /// </summary>
    public partial class MainWindow : Window
    {
        List<string> users = new List<string>();
        List<Button[]> user_buttons;
        List<Label[]> user_labels;
        List<ProgressBar> user_bars;
        
        public MainWindow()
        {
            InitializeComponent();
            InitializeUsers();
        }

        private void InitializeUsers()
        {
            this.users = File.ReadAllLines("users.txt").ToList<string>();

            this.user_buttons = new List<Button[]> { new Button[] { DisableOne, RestartOne }, new Button[] { DisableTwo, RestartTwo },
                new Button[] { DisableThree, RestartThree }, new Button[] { DisableFour, RestartFour },
                new Button[] { DisableFive, RestartFive }, new Button[] { DisableSix, RestartSix } };

            this.user_labels = new List<Label[]> { new Label[] {FQLabelOne, FTLabelOne, FRLabelOne},
                new Label[] {FQLabelTwo, FTLabelTwo, FRLabelTwo}, new Label[] {FQLabelThree, FTLabelThree, FRLabelThree},
                new Label[] {FQLabelFour, FTLabelFour, FRLabelFour}, new Label[] {FQLabelFive, FTLabelFive, FRLabelFive},
                new Label[] {FQLabelSix, FTLabelSix, FRLabelSix}};

            this.user_bars = new List<ProgressBar> { ProgressOne, ProgressTwo, ProgressThree, ProgressFour, ProgressFive, ProgressSix };

            for (int index = 0; index < this.users.Count; index++)
            {
                this.user_buttons[index][0].IsEnabled = true;
            }
        }
            
        private void StartButton_Click(object sender, RoutedEventArgs e)
        {
            string ques_num = NumberText.Text;
            if (String.IsNullOrEmpty(ques_num))
            {
                MessageBox.Show("Input number to ASK box before starting");
                return;
            }

            foreach (string line in this.users)
            {
                if (null != line)
                {
                    string[] user_info = line.Split(' ');
                    QuoraHandler.StartScript(user_info[0], user_info[1], user_info[2], ques_num);
                }
            }

            for (int index = 0; index < this.users.Count; index++)
            {
                if (null != user_buttons[index])
                {
                    this.user_buttons[index][1].IsEnabled = true;
                    this.user_bars[index].Maximum = Int32.Parse(ques_num);
                }
            }
            StartButton.IsEnabled = false;

            Thread updater = new Thread(FormUpdater);
            updater.Start();
        }

        private void FormUpdater()
        {
            while (QuoraHandler.ScriptsRunning())
            {
                for (int index = 0; index < this.users.Count; index++)
                {
                    if (null != users[index])
                    {
                        string username = users[index].Split(' ')[0];
                        Dictionary<string, int> data = null;
                        int counter = 0;
                        while(null == data && counter < 3) 
                        {
                            Thread.Sleep(1000);
                            data = QuoraHandler.GetJson(username);
                            counter++;
                        }

                        if (null != data)
                        {
                            Dispatcher.Invoke(() =>
                            {
                                user_bars[index].Value = data["AQ"];
                                user_labels[index][0].Content = data["FQ"];
                                user_labels[index][1].Content = data["FT"];
                                user_labels[index][2].Content = data["FR"];
                            });
                        }
                    }
                }
                Thread.Sleep(10000);
            }
            QuoraHandler.RemoveJson();
        }

        private void Disable(int index)
        {
            if (QuoraHandler.initiated_users.Count != 0)
            {
                string[] user_info = this.users[index].Split(' ');
                string username = user_info[0];

                Process p = QuoraHandler.initiated_users[username];
                p.Kill();
                p.Dispose();
            }

            this.user_buttons[index][0].IsEnabled = false;
            this.user_buttons[index][1].IsEnabled = false;
            this.user_bars[index].Value = 0;
            foreach (Label l in this.user_labels[index])
            {
                l.Content = "";
            }

            this.users[index] = null;
            this.user_buttons[index] = null;
        }

        private void Restart(int index)
        {
            string[] user_info = this.users[index].Split(' ');
            string username = user_info[0];

            Process p = QuoraHandler.initiated_users[username];
            p.Kill();

            Thread.Sleep(2000);

            p.Start();
        }

        private void DisableOne_Click(object sender, RoutedEventArgs e)
        {
            Disable(0);
        }

        private void RestartOne_Click(object sender, RoutedEventArgs e)
        {
            Restart(0);
        }

        private void DisableTwo_Click(object sender, RoutedEventArgs e)
        {
            Disable(1);
        }

        private void RestartTwo_Click(object sender, RoutedEventArgs e)
        {
            Restart(1);
        }

        private void DisableThree_Click(object sender, RoutedEventArgs e)
        {
            Disable(2);
        }

        private void RestartThree_Click(object sender, RoutedEventArgs e)
        {
            Restart(2);
        }

        private void DisableFour_Click(object sender, RoutedEventArgs e)
        {
            Disable(3);
        }

        private void RestartFour_Click(object sender, RoutedEventArgs e)
        {
            Restart(3);
        }

        private void DisableFive_Click(object sender, RoutedEventArgs e)
        {
            Disable(4);
        }

        private void RestartFive_Click(object sender, RoutedEventArgs e)
        {
            Restart(4);
        }

        private void DisableSix_Click(object sender, RoutedEventArgs e)
        {
            Disable(5);
        }

        private void RestartSix_Click(object sender, RoutedEventArgs e)
        {
            Restart(5);
        }
    }
}
