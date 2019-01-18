classdef Node
    
    properties
        x
        y
        isBase
        name
    end
    
    methods
        function obj = Node(x,y,isBase,name)
            obj.x = x;
            obj.y = y;
            obj.isBase = isBase;
            obj.name = name;
        end
    end
    
end

