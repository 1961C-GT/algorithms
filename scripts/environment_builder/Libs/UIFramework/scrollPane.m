function [fh, handles] = scrollPane(handles,varargin)
    % scrollPane  Creates a scroll panel that can house anchored items.
    % Example Usage:
    %    [box handles] = scrollPane(handles,'Parent',handles.someElement,...
    %       'location','top','position','[0 0 0 20]);
    %
    %   Must specify:
    %        Parent        - The anchoredContentPanel's Parent
    %        Location      - Anchor Location (Top,Bottom,Left,Right,Center,Expand)
    %        Position      - Position vector associated with the chosen location
    %
    %   See also anchoredContentPanel, anchoredPanel, anchoredElement.
    
    if verLessThan('matlab','8.4')
        warning('The Scroll Pane is not supported in versions before Matlab 2014b');
    end
    
    args = {'units','pixels'};
    update = 0;
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
                        error('Location argument must be a string (Top|Bottom|Left|Right|Center)');
                    end
                case 'position'
                    if (length(arg) == 4)
                        pos = arg;
                    else
                        error('Position must contain 4 elements.');
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
                case 'units'
                    warning('Units are set by the anchor system. This argument will be ignored');
                case 'tag'
                    warning('The Tag is used identify slider panels in the handle tree. This argument cannot be externally set.');
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
    
    % Name
    index = sum(cell2mat(strfind(fieldnames(handles),'ScrollPanel')))+1;
    name = ['ScrollPanel' num2str(index)];
    
    handles.(name).panel = uipanel(args{:},'tag',name,'parent',parent,'units','pixels');
    handles = variableSize(handles,handles.(name).panel,pos,loc,update);
    
    % Content Panel
    handles.(name).right = uipanel('bordertype','none','units','pixels','parent',handles.(name).panel);
    handles = variableSize(handles,handles.(name).right,[0 0 15 0],'expand',0);
    
    % Slider
    handles.(name).left = uipanel('bordertype','none','units','pixels','parent',handles.(name).panel);
    handles = variableSize(handles,handles.(name).left,[12 6 -5 15],'right',0);
    handles.(name).slider = uicontrol('style','slider','parent',handles.(name).left,'units',...
        'normalized','position',[0 0 1 1],'sliderstep',[0.1 0.3],'callback',{@slider,handles.f});
    
    handles.(name).update = update;
    set(handles.(name).right,'Tag','slider');
    fh = handles.(name).right;
    
end