using System;
using System.Collections.Generic;
using System.ComponentModel;
using System.Data;
using System.Drawing;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.Windows.Forms;

namespace T_Rex_Runner
{
    public partial class Form1 : Form
    {
        bool jumping = false;
        int jumpSpeed;
        int force = 12;
        int score = 0;
        int obstacleSpeed = 10;
        Random rand = new Random();
        int position;
        bool isGameOver = false;
        int yPos;


        public Form1()
        {
            InitializeComponent();
            this.Text = "T-Rex Runner: Part 2";
            GameReset();
        }

        private void MainGameTimerEvent(object sender, EventArgs e)
        {
            int yGoal = 500;
            trex.Top += jumpSpeed;
            yPos =  367-trex.Top ;
            
            //txtScore.Text = "Score: " + score;
            if (score == 0)
            {
                txtScore.Text = "Score: 0 - Press spacebar to jump";
            }
            else
            {
                txtScore.Text = "Score: " + score;
            }




            if (jumping == true && force < 0)
            {
                jumping = false;
            }

            if (jumping == true)
            {
                jumpSpeed = -12;
                force -= 1;
            }
            else
            {
                jumpSpeed = 12;
            }


            if (trex.Top > 366 && jumping == false)
            {
                force = 12;
                trex.Top = 367;
            
                jumpSpeed = 0;
            }

            
            foreach(Control x in this.Controls)
            {
                if (x is PictureBox && (string)x.Tag == "obstacle")
                {
                    x.Left -= obstacleSpeed;

                    if (x.Left < -100)
                    {
                        x.Left = this.ClientSize.Width + rand.Next(200, 500) + (x.Width * 15);
                        score++;
                    }

                    if (trex.Bounds.IntersectsWith(x.Bounds))
                    {
                        gameTimer.Stop();
                        trex.Image = Properties.Resources.dead;

                        if (score != 0)
                        {
                            txtScore.Text += " - Press r to restart the game! - Make y > 500 to win!";
                        }
                        else
                        {
                            txtScore.Text = "Score: 0 - Press r to restart the game!";
                        }
                       
                     
                        isGameOver = true;
                    }
                }
            }

            if (yPos > yGoal && jumping==true)
            {

                gameTimer.Stop();
                txtScore.Text = "Y-position is > "+yGoal+" - You WIN! WMG{pl345E_s7Op_ch3At!nG}";
                isGameOver=true;

            }


            if (score == 5)
            {
                obstacleSpeed += 1;
            }

            if (score == 10)
            {
                obstacleSpeed += 1;
            }

            if (score == 15)
            {
                obstacleSpeed += 1;
            }
            if (score == 20)
            {
                obstacleSpeed += 1;
            }

            if (score == 25)
            {
                obstacleSpeed += 1;
            }
            if (score == 32)
            {
                obstacleSpeed += 2;
            }
            if (score == 40)
            {
                obstacleSpeed += 5;
            }
        }

        private void keyisdown(object sender, KeyEventArgs e)
        {
            if (e.KeyCode == Keys.Space && jumping == false)
            {
                jumping = true;
            }
        }

        private void keyisup(object sender, KeyEventArgs e)
        {
            if (jumping == true)
            {
                jumping = false;
            }

            if (e.KeyCode == Keys.R && isGameOver == true)
            {
                GameReset();
            }
        }

        private void GameReset()
        {
            force = 12;
            jumpSpeed = 0;
            jumping = false;
            score = 0;
            obstacleSpeed = 10;
            txtScore.Text = "Score: " + score;
            trex.Image = Properties.Resources.running;
            isGameOver = false;
            trex.Top = 367;

            foreach (Control x in this.Controls)
            {

                if (x is PictureBox && (string)x.Tag == "obstacle")
                {
                    position = this.ClientSize.Width + rand.Next(500, 800) + (x.Width * 10);

                    x.Left = position;
                }
            }

            gameTimer.Start();

        }
    }
}
