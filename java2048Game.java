/**
 * @author Windard Yang
 * @time 2016-2-7
 * @email 1106911190@qq.com
 */
import java.awt.*;
import java.util.*;
import javax.swing.*;
import java.awt.event.*;
import java.io.*;
import javax.imageio.ImageIO;

class MyCanvas extends Canvas {
	int[][] tiles = new int[4][4];
	int best;
	int score;
	int overed;
	int colOver;
	int rowOver;

	public MyCanvas(){

	}

	static int randint(int i){
		Random r = new Random();
		return r.nextInt(i);
	}

	static int randomColor(int rate){
		int i = randint(rate+1);
		if(i<rate){
			return 2;
		}else{
			return 4;
		}
	}

	static Color getBackground(int num){
		switch(num){
			case 2:return new Color(0xeee4da);
			case 4:return new Color(0xede0c8);
			case 8:return new Color(0xf2b179);
			case 16: return new Color(0xf59563);
			case 32: return new Color(0xf67c5f);
			case 64: return new Color(0xf65e3b);
			case 128: return new Color(0xedcf72);
			case 256: return new Color(0xedcc61);
			case 512: return new Color(0xedc850);
			case 1024: return new Color(0xedc53f);
			case 2048: return new Color(0xedc22e);	
		}
		return new Color(0xcdc1b4);
	}

	protected int isFulled(){
		for(int i=0;i<4;i++){
			for(int j=0;j<4;j++){
				if(this.tiles[i][j]==0){
					return 0;
				}
			}
		}
		return 1;
	}

	protected void isOvered(){
		this.rowOver = 0;
		this.colOver = 0;
		colMove("right",false);
		rowMove("down",false);
		if(this.rowOver==1&&this.colOver==1&&isFulled()==1){
			gameOver();
		}
		if(this.score>this.best){
			this.best = this.score;
		}
	}

	protected void gameOver(){
		Object[] options = { "Yes", "No" };
		int n = JOptionPane.showOptionDialog(this,
				"Game Over , Do You Want To Restart ?",
				"Chose To Restart or Exit", JOptionPane.YES_NO_OPTION,
				JOptionPane.QUESTION_MESSAGE, null, options,options[0]);
		if(n==JOptionPane.YES_OPTION){
			resetGame();
		}else{
			System.exit(0);
		}		
	}

	protected void resetGame(){
		randomInit();
		repaint();
	}

	public void createColor(int num){
		int i,j;
		while(true){
			i = randint(4);
			j = randint(4);
			if(this.tiles[i][j]==0){
				this.tiles[i][j] = randomColor(num);
				break;
			}else{
				continue;
			}
		}
	}

	public void colMove(String direction,boolean temp){
		int 	i,j;
		int 	firstNumLocation = -1;
		int 	firstZeroLocation = -1;
		int 	firstNumValue = 0;
		int 	bigEnd;
		int 	diff=0;
		int[][] 	myTiles = new int[4][4];
		for(i=0;i<4;i++){
			for(j=0;j<4;j++){
				myTiles[i][j] = this.tiles[i][j];
			}
		}
		for(i=0;i<4;i++){
			firstNumLocation = -1;
			firstZeroLocation = -1;
			for(j=0;j<4;j++){
				if(direction.equals("right")){
					bigEnd = 3-j;
				}else{
					bigEnd = j;
				}
				if(this.tiles[i][bigEnd]!=0){
					if(firstNumLocation==-1&&firstZeroLocation==-1){
						firstNumLocation = bigEnd;
						firstNumValue = this.tiles[i][bigEnd];
					}else if(firstNumLocation!=-1&&firstZeroLocation==-1){
						if(this.tiles[i][bigEnd]==firstNumValue){
							firstNumValue*=2;
							if(temp)
								this.score+=firstNumValue;
							this.tiles[i][firstNumLocation]=firstNumValue;
							this.tiles[i][bigEnd] = 0;
							if(direction.equals("right")){
								firstZeroLocation = firstNumLocation-1;
							}else{
								firstZeroLocation = firstNumLocation+1;
							}
							firstNumLocation = -1;
						}else{
							if(direction.equals("right")){
								firstNumLocation--;
							}else{
								firstNumLocation++;
							}
							firstNumValue = this.tiles[i][bigEnd];
						}
					}else if(firstNumLocation==-1&&firstZeroLocation!=-1){
						firstNumLocation = firstZeroLocation;
						firstNumValue = this.tiles[i][bigEnd];
						this.tiles[i][firstZeroLocation] = firstNumValue;
						this.tiles[i][bigEnd] = 0;
						if(direction.equals("right")){
						    firstZeroLocation--;
						}else{
						    firstZeroLocation++;
						}
					}else{
						if(this.tiles[i][bigEnd]==firstNumValue){
							firstNumValue*=2;
							if(temp)
								this.score+=firstNumValue;
							this.tiles[i][firstNumLocation] = firstNumValue;
							this.tiles[i][bigEnd] = 0;
							firstZeroLocation = -1;
						}else{
							if(direction.equals("right")){
								firstNumLocation--;
								firstZeroLocation--;
							}else{
								firstNumLocation++;
								firstZeroLocation++;
							}
							firstNumValue = this.tiles[i][bigEnd];
							this.tiles[i][firstNumLocation] = firstNumValue;
							this.tiles[i][bigEnd]=0;
						}
					}

				}else{
					if(firstZeroLocation==-1){
						firstZeroLocation = bigEnd;
					}
				}
			}
		}
		for(i=0;i<4;i++){
			for(j=0;j<4;j++){
				if(myTiles[i][j]!=this.tiles[i][j]){
					diff=1;
					break;
				}
			}
		}
		if(temp){
			if(diff==1&&isFulled()!=1){
				createColor(9);
			}
			repaint();
		}else{
			if(diff!=1){
				this.colOver = 1;
			}
			for(i=0;i<4;i++){
				for(j=0;j<4;j++){
					this.tiles[i][j] = myTiles[i][j];
				}
			}
		}
	}

	public void rowMove(String direction,boolean temp){
		int 	i,j;
		int 	firstNumLocation = -1;
		int 	firstZeroLocation = -1;
		int 	firstNumValue = 0;
		int 	bigEnd;
		int 	diff=0;
		int[][] 	myTiles = new int[4][4];
		for(i=0;i<4;i++){
			for(j=0;j<4;j++){
				myTiles[i][j] = this.tiles[i][j];
			}
		}
		for(i=0;i<4;i++){
			firstNumLocation = -1;
			firstZeroLocation = -1;
			for(j=0;j<4;j++){
				if(direction.equals("down")){
					bigEnd = 3-j;
				}else{
					bigEnd = j;
				}
				if(this.tiles[bigEnd][i]!=0){
					if(firstNumLocation==-1&&firstZeroLocation==-1){
						firstNumLocation = bigEnd;
						firstNumValue = this.tiles[bigEnd][i];
					}else if(firstNumLocation!=-1&&firstZeroLocation==-1){
						if(this.tiles[bigEnd][i]==firstNumValue){
							firstNumValue*=2;
							if(temp)
								this.score+=firstNumValue;
							this.tiles[firstNumLocation][i]=firstNumValue;
							this.tiles[bigEnd][i] = 0;
							if(direction.equals("down")){
								firstZeroLocation = firstNumLocation-1;
							}else{
								firstZeroLocation = firstNumLocation+1;
							}
							firstNumLocation = -1;
						}else{
							if(direction.equals("down")){
								firstNumLocation--;
							}else{
								firstNumLocation++;
							}
							firstNumValue = this.tiles[bigEnd][i];
						}
					}else if(firstNumLocation==-1&&firstZeroLocation!=-1){
						firstNumLocation = firstZeroLocation;
						firstNumValue = this.tiles[bigEnd][i];
						this.tiles[firstZeroLocation][i] = firstNumValue;
						this.tiles[bigEnd][i] = 0;
						if(direction.equals("down")){
						    firstZeroLocation--;
						}else{
						    firstZeroLocation++;
						}
					}else{
						if(this.tiles[bigEnd][i]==firstNumValue){
							firstNumValue*=2;
							if(temp)
								this.score+=firstNumValue;
							this.tiles[firstNumLocation][i] = firstNumValue;
							this.tiles[bigEnd][i] = 0;
							firstZeroLocation = -1;
						}else{
							if(direction.equals("down")){
								firstNumLocation--;
								firstZeroLocation--;
							}else{
								firstNumLocation++;
								firstZeroLocation++;
							}
							firstNumValue = this.tiles[bigEnd][i];
							this.tiles[firstNumLocation][i] = firstNumValue;
							this.tiles[bigEnd][i]=0;
						}
					}

				}else{
					if(firstZeroLocation==-1){
						firstZeroLocation = bigEnd;
					}
				}
			}
		}
		for(i=0;i<4;i++){
			for(j=0;j<4;j++){
				if(myTiles[i][j]!=this.tiles[i][j]){
					diff=1;
					break;
				}
			}
		}
		if(temp){
			if(diff==1&&isFulled()!=1){
				createColor(9);
			}
			repaint();
		}else{
			if(diff!=1){
				this.rowOver = 1;
			}
			for(i=0;i<4;i++){
				for(j=0;j<4;j++){
					this.tiles[i][j] = myTiles[i][j];
				}
			}
		}
	}

	protected void randomInit(){
		int	i,j;
		int	times = randint(2)+2;
		for(i=0;i<4;i++){
			for(j=0;j<4;j++){
				this.tiles[i][j]=0;
			}
		}		
		for(i=0;i<times;i++){
			createColor(4);
		}
		this.score = 0;
		this.overed = 0;
	}

	public void paint(Graphics g){
		g.setColor(new Color(0xbbada0));
		g.fillRect(0, 0, this.getSize().width, this.getSize().height);	
		g.setColor(new Color(0x776e65));
		g.fillRoundRect(25,20,140,50,10,10);
		g.fillRoundRect(175,20,140,50,10,10);
		g.setColor(new Color(0xcdc1b4));
		g.setFont(new Font("Arial", Font.PLAIN , 20));
		g.drawString("SCORE: ",35,52);
		g.drawString("BEST: ",185,52);
		g.setColor(new Color(255,255,255));
		g.drawString(String.valueOf(this.score),115,52);
		g.drawString(String.valueOf(this.best),250,52);
		for(int i=0;i<4;i++){
			for(int j=0;j<4;j++){
				g.setColor(getBackground(this.tiles[i][j]));
				g.fillRoundRect(20+j*80,90+i*80,65,65,10,10);
				if(this.tiles[i][j]!=0){
					if(this.tiles[i][j]<15){
						g.setColor(new Color(100,100,100));
					}else{
						g.setColor(new Color(255,255,255));
					}
					int fontSize = this.tiles[i][j]<511?26:20;
					Font f = new Font("Arial", Font.BOLD , fontSize);
					g.setFont(f);					
					String s = String.valueOf(this.tiles[i][j]);
					final FontMetrics fm = getFontMetrics(f);
					final int w = fm.stringWidth(s);	
					g.drawString(s,53+j*80-w/2,132+i*80);
				}
			}
		}		
	}

}

public class java2048Game{
	public static void main(String[] args){
		MyCanvas cv = new MyCanvas();
		JFrame f = new JFrame("2048 Game");
		f.setResizable(false);
		f.setSize(350,450);
		f.add(cv);
		f.setVisible(true);		
		f.setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
		// f.setDefaultCloseOperation(WindowConstants.EXIT_ON_CLOSE);
		try{
			f.setIconImage(ImageIO.read(new File("2048.ico")));
		}catch(Exception e){
			e.printStackTrace();
		}
		f.setLocationRelativeTo(null);
		cv.randomInit();
		f.addKeyListener(new keyHandler(cv));
	}
}

class keyHandler implements KeyListener{
	MyCanvas cv = new MyCanvas();

	public keyHandler(MyCanvas cv){
		this.cv = cv;
	}

	public void keyPressed(KeyEvent e){
		switch (e.getKeyCode()){
			case KeyEvent.VK_LEFT : this.cv.colMove("left",true);this.cv.isOvered();break;
			case KeyEvent.VK_RIGHT : this.cv.colMove("right",true);this.cv.isOvered();break;
			case KeyEvent.VK_DOWN : this.cv.rowMove("down",true);this.cv.isOvered();break;
			case KeyEvent.VK_UP : this.cv.rowMove("up",true);this.cv.isOvered();break;
			case KeyEvent.VK_ESCAPE : this.cv.resetGame();this.cv.isOvered();break;
		}
	}

	public void keyReleased(KeyEvent e){
	}

	public void keyTyped(KeyEvent e){
	}	

}
