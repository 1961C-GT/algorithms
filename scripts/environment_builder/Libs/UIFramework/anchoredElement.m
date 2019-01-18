function [fh, handles] = anchoredElement(handles,varargin)
% anchoredElement  Creates an anchored uicontrol element.
% Example Usage:
%     [box handles] = anchoredElement(handles,'Parent',...
%        handles.someElement, 'location','top','position','[0 0 0 20],...
%        'style','pushbutton','string','this is a test');
%
%   Must specify:
%        Parent        - The anchoredContentPanel's Parent
%        Location      - Anchor Location (Top,Bottom,Left,Right,Center,Expand)
%        Position      - Position vector associated with the chosen location
%        Style Options - Required arguments for the chosen uicontrol
%                        element (eg, style or string)
%
%   See also editBox, titleElement.
bordertype = 'none';
update = 0;
ratios = [0 1];
args = {'units','normalized'};
skip = false;
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
            case 'ratios'
                if (length(arg) == 2)
                    ratios = arg;
                else
                    error('Ratios must contain the following: [Lwall-to-element, element-to-Rwall]');
                end
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
            case 'bordertype'
                bordertype = arg;
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
div = uipanel('parent',parent,'units','pixels','bordertype',...
    bordertype);
%         guidata(handles.f, handles);
handles = variableSize(handles,div,pos,loc,update);
%         guidata(handles.f,handles);
% Had to change from outerPosition to Position for V2013b
fh = uicontrol(args{:},'Position',[ratios(1),0,ratios(2)-ratios(1),1],...
    'Parent',div);
end