import bpy
import random
from bge import constraints, events, logic, render, types
from mathutils import Vector
from math import radians


class Map:

    def __init__( self, size=40, random=80 ):
        
        self.filds = {}
        self.size = size
        self.random = random
        self.ronds = self.size * self.size
        self.out = ""
        self.start_x = 0
        self.start_y = 0
        
        self.genMap()

    def setFild( self, x, y ):
        
        ret = {
            0 : x,
            1 : y,
        }
        
        return ret
    
    def updateFild( self ):
        
        fild = {
            0 : self.setFild( 1, 0 ),
            1 : self.setFild( -1, 0 ),
            2 : self.setFild( 0, 1 ),
            3 : self.setFild( 0, -1 ),
        }[ random.randint( 0, 3 ) ]
        
        return fild
    
    def genMap( self ):

        for i in range( 0, self.size ):
            for j in range( 0, self.size ):
                self.filds[ i, j ] = 0
        
        fild = self.updateFild()
        
        for i in range( 0, self.ronds ):
            
            self.filds[ self.start_x, self.start_y ] = 1
            
            if random.randint( 0, 100 ) < self.random :
                fild = self.updateFild()
            
            if self.start_x + fild[ 0 ] >= 0 and self.start_x + fild[ 0 ] <= self.size:
                if self.start_y + fild[ 1 ] >= 0 and self.start_y + fild[ 1 ] <= self.size:
                    self.start_x = self.start_x + fild[ 0 ]
                    self.start_y = self.start_y + fild[ 1 ]
                    self.filds[ self.start_x, self.start_y ] = 1
    
    def getMap( self ):
        return self.filds
    
    def getValue( self, x, y ):
        
        out = 0
        
        if x > -1 and x < self.size and y > -1 and y < self.size:
            out = self.filds[ x, y ]
            
        return out
    
    def printMap( self ):
        
        print( "---- Start Map ----" )
        
        for i in range( 0, self.size ):
            out = ""
            for j in range( 0, self.size ):
                out = out + str( self.filds[ i, j ] ) + " "
            print( out )
        
        print( "---- End Map ----" )

class Level:
    
    def __init__( self ):
        
        self.scene = logic.getCurrentScene()
        self.spawner = self.scene.objects[ "Spawner" ]
        
        self.mapSize = 40
        self.map = Map( self.mapSize, 5 )
        
        self.tileSize = 4
        
        self.north = 0
        self.east = 1
        self.south = 2
        self.west = 3
        
        pass
        
    def place( self, orientation, name ):
        
        obj = self.scene.addObject( name, self.spawner )
        
        if orientation == "North" or orientation == 0:
            
            obj.worldOrientation = ( 0, 0, radians( 180 ) )
            obj.worldPosition += Vector( ( self.tileSize, self.tileSize, 0 ) )
            pass
        
        elif orientation == "East" or orientation == 1:
            
            obj.worldOrientation = ( 0, 0, radians( 90 ) )
            obj.worldPosition += Vector( ( self.tileSize, 0, 0 ) )
            pass
        
        elif orientation == "West" or orientation == 3:
            
            obj.worldOrientation = ( 0, 0, radians( -90 ) )
            obj.worldPosition += Vector( ( 0, self.tileSize, 0 ) )
            pass
        
        pass
    
    def move( self, orientation ):
        
        if orientation == "North" or orientation == 0:
            
            self.spawner.worldPosition += Vector( ( 0, self.tileSize, 0 ) )
            pass
        
        elif orientation == "East" or orientation == 1:
            
            self.spawner.worldPosition+= Vector( ( self.tileSize, 0, 0 ) )
            pass
        
        elif orientation == "West" or orientation == 3:
            
            self.spawner.worldPosition += Vector( ( -self.tileSize, 0, 0 ) )
            pass
        
        else:
            
            self.spawner.worldPosition += Vector( ( 0, -self.tileSize, 0 ) )
            pass
        
        pass
    
    
    def moveTo( self, x, y ):
        
        self.spawner.worldPosition = Vector( ( x*self.tileSize, y*self.tileSize, 0 ) )
        
    def genStructure( self ):
        
        for x in range( 0, self.mapSize ):
            for y in range( 0, self.mapSize ):
                
                self.moveTo( x, y )
                
                if self.map.getValue( x, y ) > 0:
                    self.place( self.south, "Floor" )
                    self.place( self.south, "Roof" )
                    
                    if self.map.getValue( x-1, y ) < 1:
                        self.place( self.west, "Wall" )
                        
                    if self.map.getValue( x+1, y ) < 1:
                        self.place( self.east, "Wall" )
                        
                    if self.map.getValue( x, y-1 ) < 1:
                        self.place( self.south, "Wall" )
                    
                    if self.map.getValue( x, y+1 ) < 1:
                        self.place( self.north, "Wall" )
    
    def genCorners( self ):
        
        for x in range( 0, self.mapSize ):
            for y in range( 0, self.mapSize ):
                
                self.moveTo( x, y )
                
                if self.map.getValue( x, y ) > 0:
                    
                    if self.map.getValue( x-1, y ) < 1 and self.map.getValue( x, y-1 ) < 1:
                        self.place( self.south, "EdgeCorner" )
                    
                    if self.map.getValue( x+1, y ) < 1 and self.map.getValue( x, y-1 ) < 1:
                        self.place( self.east, "EdgeCorner" )
                    
                    if self.map.getValue( x+1, y ) < 1 and self.map.getValue( x, y+1 ) < 1:
                        self.place( self.north, "EdgeCorner" )
                    
                    if self.map.getValue( x-1, y ) < 1 and self.map.getValue( x, y+1 ) < 1:
                        self.place( self.west, "EdgeCorner" )
    
    def genStraights( self ):
        
        for x in range( 0, self.mapSize ):
            for y in range( 0, self.mapSize ):
                
                self.moveTo( x, y )
                
                if self.map.getValue( x, y ) > 0:
                    
                    if self.map.getValue( x-1, y ) > 0 and self.map.getValue( x, y-1 ) < 1 and self.map.getValue( x-1, y-1 ) < 1:
                        self.place( self.south, "EdgeStraight" )
                    
                    if self.map.getValue( x+1, y ) > 0 and self.map.getValue( x, y+1 ) < 1 and self.map.getValue( x+1, y+1 ) < 1:
                        self.place( self.north, "EdgeStraight" )
                    
                    if self.map.getValue( x, y-1 ) > 0 and self.map.getValue( x+1, y ) < 1 and self.map.getValue( x+1, y-1 ) < 1:
                        self.place( self.east, "EdgeStraight" )
                        
                    if self.map.getValue( x, y+1 ) > 0 and self.map.getValue( x-1, y ) < 1 and self.map.getValue( x-1, y+1 ) < 1:
                        self.place( self.west, "EdgeStraight" )
    
    def gen( self ):
        
        self.genStructure()
        self.genCorners()
        self.genStraights()

level = Level()

def gen():
    level.gen()
