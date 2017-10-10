import java.awt.*;
import java.awt.event.*;
import java.awt.geom.*;
import java.util.ArrayList;
import javax.swing.*;


public class balle extends JFrame {
/*Bouttons*/
  private static final long serialVersionUID = 1L;
  private JButton ajouter = new JButton("  +  ");
  private JButton supprimer = new JButton("  -  ");
  private JButton pause = new JButton("Stop");
  private JButton sortir = new JButton("Sortir");
  private JPanel boutons = new JPanel();
  private Panneau panneau = new Panneau();

//Classe Balle
  public balle() 
  {
        super("Balles en Mouvement");
        panneau.setBackground(Color.white);
        add(panneau);
        add(boutons, BorderLayout.SOUTH);
        boutons.add(ajouter);
        boutons.add(supprimer);
        boutons.add(pause);
        boutons.add (sortir);
//action ajoute
        ajouter.addActionListener(new ActionListener() 
        {
           public void actionPerformed(ActionEvent e) 
           {
              ajoutBalle();
           }
        });
//action supprime
        supprimer.addActionListener(new ActionListener() 
        {
           public void actionPerformed(ActionEvent e) 
           {
              supprimBalle();
           }
        }); 
//action pause
        pause.addActionListener(new ActionListener() 
        {
           public void actionPerformed(ActionEvent e) 
           {
          	 try 
          	 {
  				Thread.sleep(5000);
  			} catch (InterruptedException e1) 
  			{
  				// TODO Auto-generated catch block
  				e1.printStackTrace();
  			}
           }
        });
//action sortir      
        sortir.addActionListener(new ActionListener() 
        {
            public void actionPerformed(ActionEvent e) 
            {
          	 System.exit(0);
            }
         });
        setSize(600, 600);
        setLocationRelativeTo(null);
        setDefaultCloseOperation(EXIT_ON_CLOSE);
        setVisible(true);
     }
     
//ajouter balle
    private void ajoutBalle() 
    {
      Balle balle = new Balle();      
      panneau.ajout(balle);
      new Thread(new BalleSeparee(balle)).start();
    }
//supprimer ball
    private void supprimBalle()
    {
      Balle balle = new Balle();
      panneau.supprime(balle);
      new Thread(new BalleSeparee(balle)).start();
    }

     //=====================Autres_Class====================>

//balle separee
     private class BalleSeparee implements Runnable 
     {
        private Balle balle;

        public BalleSeparee(Balle balle) 
        {
            this.balle = balle;
        }
        
        public void run() 
        {
           try 
           {
              while(true)
              {
                 balle.deplace(panneau.getBounds());
                 panneau.repaint();
                 Thread.sleep(20);
              }
           }
           catch (InterruptedException ex) { }
        }
     }

//paneau
     private class Panneau extends JPanel 
     {
        private ArrayList<Balle> balles = new ArrayList<Balle>();
    //ajouter une balle a la liste des balles
        public void ajout(Balle balle) 
        {
           balles.add(balle);
           
        }
      //supprimer une balle de la liste des balles
        public void supprime(Balle balle)
        {
      	  balles.remove(balle);
        }
      //dessiner les balles dans le paneau
        @Override
        protected void paintComponent(Graphics g) 
        {
           super.paintComponent(g);
           Graphics2D surface = (Graphics2D) g;
           g.setColor(Color.black);
           for (Balle balle : balles) surface.fill(balle.getForme());
           
        }
     }

    private class Balle 
    {
        private double x, y, dx=10, dy=10; //localisation et vitesses

    //deplacement des balles
        public void deplace(Rectangle2D zone) 
        {
           x+=dx;
           y+=dy;
           if (x < zone.getMinX()) { x = zone.getMinX();  dx = -dx; }
           if (x+11 >= zone.getMaxX()) { x = zone.getMaxX() - 11;  dx = -dx; }
           if (y < zone.getMinY()) { y = zone.getMinY();  dy = -dy; }
           if (y+11 >= zone.getMaxY()) { y = zone.getMaxY() - 11;  dy = -dy; }
        }
        
    //dessiner un eclipse
          public Ellipse2D getForme() 
          {
        	  
             return new Ellipse2D.Double(x, y, 25, 25); //dimensions
          }
       }

//================>       Main      <===================\\
     public static void main(String[] args) 
     { 
  	   new balle(); 
     }
}