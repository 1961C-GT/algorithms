function [fh, handles] = anchoredPanel(handles,varargin)
% anchoredPanel  Creates an anchored panel.
% Example Usage:
%    [box handles] = anchoredPanel(handles,'Parent',handles.someElement,...
%       'location','top','position','[0 0 0 20]);
%
%   Must specify:
%        Parent        - The anchoredContentPanel's Parent
%        Location      - Anchor Location (Top,Bottom,Left,Right,Center,Expand)
%        Position      - Position vector associated with the chosen location
%
%   See also anchoredContentPanel, scrollPane, anchoredElement.
bordertype = 'none';
update = 0;
args = {'units','normalized'};
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
            case 'location'
                if (ischar(arg))
                    loc = arg;
                else
                    error('Location argument must be a string (Top|Bottom|Left|Right|Center|Expand)');
                end
            case 'position'
                if (length(arg) == 4)
                    pos = arg;
                else
                    error('Position must contain 4 elements');
                end
            case 'bordertype'
                bordertype = arg;
            case 'update'
                if (ischar(arg))
                    if (strcmpi(arg,'dynamic'))
                        update = 0;
                    elseif (strcmpi(arg,'static'))
                        update = 1;
                    elseif (strcmpi(arg,'scroll'))
                        update = 2;
                    else
                        error('Invalid update option. Must be ''dynamic'',''static'', or ''scroll''');
                    end
                else
                    error('Update option must be a string: (''dynamic''|''static''|''scroll'')');
                end
            case 'units'
                warning('Units is set by the anchor system. This argument will be ignored');
            case 'parent'
                if (ishandle(arg) && ~exist('parent','var'))
                    parent = arg;
                end
            otherwise
                args(end+1) = {vars};
                args(end+1) = {arg};
        end
        
    end
end
if(~exist('parent','var'))
    error ('Must specify a parent handle (handle OR Parent, handle)');
end
if(~exist('loc','var'))
    error ('Must specify a anchor location (Location, Top|Bottom|Left|Right|Center).');
end
if(~exist('pos','var'))
    error ('Must specify a position set (Position, [pading, offset, dim]).');
end
fh = uipanel(args{:},'parent',parent,'units','pixels','bordertype',...
    bordertype);
%         guidata(handles.f, handles);
handles = variableSize(handles,fh,pos,loc,update);
%         guidata(handles.f,handles);
end