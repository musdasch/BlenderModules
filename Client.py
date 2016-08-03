from bge import logic, events
from mathutils import Vector
import numpy
import socket
import pickle

def keyDown( key_code, status=logic.KX_INPUT_ACTIVE ):
    
    if logic.keyboard.events[ key_code ] == status:
        return True
    return False


def keyHit( key_code ):
    return keyDown( key_code, logic.KX_INPUT_JUST_ACTIVATED )

class Client:
    
    def __init__( self, server_ip="localhost", server_port=9999 ):
        
        self.socket = socket.socket( socket.AF_INET, socket.SOCK_DGRAM )
        self.socket.setblocking( False )
        
        self.serv_addr = ( server_ip, server_port )
        
        self.entities = {}
        
        self.main = self.state_sendName
        
    def state_sendName( self ):
        
        scene = logic.getCurrentScene()
        text = scene.objects[ "Name" ]
        
        if( keyHit( events.ENTERKEY ) ):
            self.socket.sendto( bytes( text[ "Text" ], "utf-8" ), self.serv_addr )
            text.endObject()
            self.main = self.state_loop
            
    def state_loop( self ):
        self.send()
        self.receive()
        
    def send( self ):
        
        list_key_stat = []
        
        kevts = logic.keyboard.events
        for k in kevts:
            s = kevts[ k ]
            if s == logic.KX_INPUT_ACTIVE:
                list_key_stat.append( ( k, s ) ) 
            
            if s == logic.KX_INPUT_JUST_RELEASED:
                list_key_stat.append( ( k, 0 ) )
        
        if len( list_key_stat ):
            self.socket.sendto( pickle.dumps( list_key_stat ), self.serv_addr )
   
    def receive( self ):
        
        while True:
            try:
                data, addr = self.socket.recvfrom( 1024 )
                
                state = pickle.loads( data )
                
                for k in state:
                    if not k in self.entities:
                        scene = logic.getCurrentScene()
                        spawner = scene.objects[ "Spawner" ]
                        entety = scene.addObject( k[ 0 ], spawner )
                        entety.children[ 0 ]["Text"] = k[ 1 ]
                        self.entities[ k ] = entety
                        
                    else:
                        entety = self.entities[ k ]
                
                    entety.worldPosition = Vector( state[ k ] )
                     
            except socket.error:
                break
            
client = Client()

def main():
    client.main()
