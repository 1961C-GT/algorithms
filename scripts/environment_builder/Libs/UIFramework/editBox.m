function [fh, handles] = editBox(handles,varargin)
% editBox  Creates an anchored panel containing a title and an edit box.
% Example Usage:
%     [box handles] = editBox(handles,'Parent',handles.someElement,...
%        'location','top','position','[0 0 0 20],'Ratios',[0 0.5 1],...
%        'Title','Some Title','DefaultText','Type Here');
%
%   Must specify:
%        Parent        - The anchoredContentPanel's Parent
%        Location      - Anchor Location (Top,Bottom,Left,Right,Center,Expand)
%        Position      - Position vector associated with the chosen location
%        Ratios        - A ratio vector from 0 to 1: [Lwall center Rwall]
%        Title         - The text title
%        Defaulttext   - The default text for the box
%
%   See also titleElement, anchoredElement.
args = {'style','edit'};
if ispc
    font = 8;
else
    font = 10;
end
skip = false;
if (~isstruct(handles))
    error ('First argument must be the GUI handle structure');
end
for i = 1:length(varargin)
    if (skip)
        skip = false;
        continue;
    end
    vars = varargin{i};
    if (length(vars) == 1 && ishandle(vars) && ~exist('parent','var'))
        parent = vars;
    elseif (ischar(vars))
        if (i+1 <= length(varargin))
            arg = varargin{i+1};
        else
            error('Found term eithout matching argument.');
        end
        skip = true;
        switch lower(vars)
            case 'fontsize'
                if (isa(arg,'numeric'))
                    font = arg;
                    args(end+1) = {'titlefontsize'};
                    args(end+1) = {arg};
                else
                    warning('Passed title font size is invalid. Using default of 12pt');
                end
            case 'parent'
                if (ishandle(arg) && ~exist('parent','var'))
                    parent = arg;
                end
            case 'defaulttext'
                if (ischar(arg))
                    default = arg;
                end
            otherwise
                args(end+1) = {vars};
                args(end+1) = {arg};
        end
    end
end
if(~exist('default','var'))
    error ('Must a default edit text (''defaulttext'', ''sometext'').');
end
if(~exist('parent','var'))
    error ('Must specify a parent handle (handle OR ''Parent'', handle)');
end

[fh, handles] = titleElement(handles,parent,args{:},'fontsize',font,...
    'string',default,'Callback',@checkContent);
end