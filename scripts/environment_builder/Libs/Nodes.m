classdef Nodes < handle
    
    properties
        nodeList
        baseList
    end
    
    methods
        function obj = Nodes()
            obj.nodeList = {};
            obj.baseList = {};
        end
        
        function list = getAll(obj)
            list = {};
            for i = 1:1:obj.numBases()
                list{end+1} = obj.baseList{i};
            end
            for i = 1:1:obj.numNodes()
                list{end+1} = obj.nodeList{i};
            end
        end
        
        function addNode(obj, x, y, name)
            obj.nodeList{end+1} = Node(x,y,false,name);
        end
        
        function addBase(obj, x, y, name)
            obj.baseList{end+1} = Node(x,y,true,name);
        end
        
        function removeNode(obj)
            obj.nodeList(end) = [];
        end
        
        function removeBase(obj)
            obj.baseList(end) = [];
        end
        
        function num = numNodes(obj)
            
            num = length(obj.nodeList);
        end
        
        function num = numBases(obj)
            num = length(obj.baseList);
        end
        
    end
    
end

