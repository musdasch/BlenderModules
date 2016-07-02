from bge import events, logic, render, types
from mathutils import Vector

class MouseLook:
    
    def __init__( self, cont ):
        
        self.cont = cont
        self.sen_mous = self.cont.sensors[ "Mouse" ]
        self.act_rotx = self.cont.actuators[ "RotX" ]
        self.act_rotz = self.cont.actuators[ "RotZ" ]
        
        self.cont.activate( self.act_rotx )
        self.cont.activate( self.act_rotz )
        
        x = render.getWindowWidth()//2
        y = render.getWindowHeight()//2
        self.screen_center = ( x, y )
        
        render.setMousePosition( * self.screen_center )
    
    def getMouseOffset( self ):
        
        vec_screencenter = Vector( self.screen_center )
        vec_mouseposition = Vector( self.sen_mous.position )
        
        return vec_mouseposition - vec_screencenter
    
    def main( self ):
        
        vec_offset = self.getMouseOffset()
        vec_offset *= -0.005
        
        self.act_rotx.dRot = [ vec_offset.y, 0, 0 ]
        self.act_rotz.dRot = [ 0, 0, vec_offset.x ]
        
        render.setMousePosition( * self.screen_center )
        

init = False
mouseLook = MouseLook( logic.getCurrentController() )

def main():
    
    global init
    
    if init:
        mouseLook.main()
    else:
        init = True
