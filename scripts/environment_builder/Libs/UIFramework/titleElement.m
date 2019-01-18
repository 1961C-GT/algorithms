function [fh, handles] = titleElement(handles,varargin)
% editBox  Creates an anchored panel containing a title and a uiControl element.
% Example Usage:
%     [box handles] = titleElement(handles,'Parent',handles.someElement,...
%        'location','top','position','[0 0 0 20],'Ratios',[0 0.5 1],...
%        'Title','Some Title','Style','pushbutton','String','Test');
%
%   Must specify:
%        Parent        - The anchoredContentPanel's Parent
%        Location      - Anchor Location (Top,Bottom,Left,Right,Center,Expand)
%        Position      - Position vector associated with the chosen location
%        Ratios        - A ratio vector from 0 to 1: [Lwall center Rwall]
%        Title         - The text title
%        Style         - The uicontrol style
%
%   See also editBox, anchoredElement.
if ispc
    font = 8;
else
    font = 10;
end
bordertype = 'none';
update = 0;
% Required so that args can be used. At least one element must be
% in it
args = {'units','normalized'};

if (~isstruct(handles))
    error ('First argument must be the GUI handle structure');
end

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
                if (length(arg) == 3)
                    ratios = arg;
                else
                    error('Ratios must contain the following: [Lwall-to-title, title-to-entry entry-to-Rwall]');
                end
            case 'title'
                if (ischar(arg))
                    title = arg;
                else
                    error('Title argument must be a string');
                end
            case 'bordertype'
                bordertype = arg;
            case 'parent'
                if (ishandle(arg) && ~exist('parent','var'))
                    parent = arg;
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
            case 'titlefontsize'
                if (isa(arg,'numeric'))
                    font = arg;
                else
                    warning('Passed title font size is invalid. Using default of 12pt');
                end
            case 'style'
                if (ischar(arg))
                    style = arg;
                else
                    error('Style argument must be a string');
                end
            otherwise
                args(end+1) = {vars};
                args(end+1) = {arg};
        end
        
    end
end
if(~exist('title','var'))
    error ('Must specify a title (''Title'', ''example'')');
end
if(~exist('loc','var'))
    error ('Must specify a anchor location (''Location'', Top|Bottom|Left|Right|Center)');
end
if(~exist('pos','var'))
    error ('Must specify a position set (''Position'', [pading, offset, dim])');
end
if(~exist('ratios','var'))
    error ('Must specify a ratio set (''Ratios'', [Lwall-to-element, element-to-Rwall])');
end
if(~exist('parent','var'))
    error ('Must specify a parent handle (handle OR ''Parent'', handle)');
end
if(~exist('style','var'))
    error ('Must specify an element style (style, (''pushbutton''|''edit'',etc...)');
end


div = uipanel('parent',parent,'units','pixels','bordertype',bordertype);
%         guidata(handles.f, handles);
handles = variableSize(handles,div,pos,loc,update);
%         guidata(handles.f,handles);
uicontrol('style','text',...
    'units','normalized',...
    'Position',[ratios(1),0,ratios(2),1],...
    'horizontalAlignment','right',...
    'string',title,...
    'fontsize',font,...
    'Parent',div);
fh = uicontrol('style',style,args{:},'Position',[ratios(2)*1.05,0,ratios(3)-ratios(2)*1.05,1],...
    'Parent',div);
end