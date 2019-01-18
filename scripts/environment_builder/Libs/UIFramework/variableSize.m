% variableSize  Sets the object to a given anchored posiiton
% Usage:
%        variableSize(handles, name within handles (or a handle), position vector
%              location string, update options);
%
% Location List : Position Vector Contents
%   - Left      : [vert pad, off from left wall, vert off from center, fixed
%                  width]
%   - Right     : [vert pad, off from right wall, vert off from center, fixed
%                  width]
%   - Center    : [fixed width, fixed height, horiz off center, vert off
%                  center]
%   - Top       : [horiz pad, off from top wall, horiz off center, fixed
%                  height]
%   - Bottom    : [horiz pad, off from bot wall, horiz off center, fixed
%                  height]
%   - expand    : [off from left wall, off from bottom wall, off from right
%                  wall, off from top wall]
%
% Update Options: Scheme
%   0    :   Dynamic Update (default option)
%   1    :   Static Update (Only first draw). For this to increase
%            speed, all children must also be set to a static update.
%   2    :   Scroll (used only for elements in a scroll panel that is a
%            static size, either 'update static' or anchored to a fixed
%            size). Children of a static scrollpanel are automatically set
%            to the Scroll update scheme.
%
%   See also anchoredElement, variableSizeManager.
function handles = variableSize(handles,name,position,location,update)
    
    if (~isstruct(handles))
        error ('First argument must be the GUI handle structure');
    end
    if (ishandle(name))
        handle = name;
        if (isfield(handles, 'anchors'))
            index = sum(cell2mat(strfind(fieldnames(handles.anchors),'el')))+1;
        else
            index = 1;
        end
        name = ['el' num2str(index)];
    else
        handle = handles.(name);
    end
    set(handle,'Units','Pixels');
    handles.anchors.(name).handle = handle;
    handles.anchors.(name).position = position;
    handles.anchors.(name).loc = location;
    handles.anchors.(name).update = update;
    if strcmpi(get(get(handle,'Parent'),'Tag'),'slider')
        handles.anchors.(name).sliderReference = get(get(get(handle,'Parent'),'Parent'),'Tag');
        handles.anchors.(name).initPos = position;
    end
    
    
end