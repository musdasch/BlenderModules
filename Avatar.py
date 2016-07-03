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


class KeyMotion:
    
    def __init__( self, cont ):
        
        self.cont = cont
        self.sen_key = self.cont.sensors[ "Keyboard" ]
        self.act_rotz = self.cont.actuators[ "RotZ" ]
        self.speed = 0.1
        self.active_key = logic.KX_INPUT_ACTIVE
        
        self.cont.activate( self.act_rotz )
    
    
    def keyDown( self, key_code ):
        
        if logic.keyboard.events[ key_code ] == self.active_key:
            return True
        return False
    
    
    def main( self ):
        
        up_down = self.keyDown( events.SKEY ) - self.keyDown( events.WKEY )
        right_left = self.keyDown( events.DKEY ) - self.keyDown( events.AKEY )

        delta = Vector( ( right_left, up_down ) )
        delta *= self.speed

        self.act_rotz.dLoc = [ delta.y, delta.x, 0 ]

     
class Avatar:
    
    def __init__( self, cont ):
        
        self.init = False
        self.mouseLook = MouseLook( cont )
        self.keyMotion = KeyMotion( cont )
    
    def main( self ):
        
        if self.init:
            self.mouseLook.main()
            self.keyMotion.main()
        else:
            self.init = True


avatar = Avatar( logic.getCurrentController() )

def main():
    avatar.main()
