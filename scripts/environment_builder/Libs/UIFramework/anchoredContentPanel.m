function [fh, handles, TopContainer] = anchoredContentPanel(handles,varargin)
% anchoredContentPanel  Creates an anchored panel with tabs.
% Example Usage:
%     [box handles] = anchoredContentPanel(handles,'Parent',...
%        handles.someElement, 'location','top','position','[0 0 0 20],...
%        'titles',{'Tab 1','Tab 2','Tab 3'});
%
%   Must specify:
%        Parent   - The panel's Parent
%        Location - Anchor Location (Top,Bottom,Left,Right,Center,Expand)
%        Position - Position vector associated with the chosen location
%        titles   - A cell of tab title names (eg. {'T1','T2','T3}
%
%   See also anchoredElement, anchoredPanel.
args = {};
update = 'dynamic';
skip = false;
high = [240 240 240]./255;
low = [210 210 210]./255;

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
                warning('Changing the border of a contentPanel is unsupported');
            case 'update'
                if (ischar(arg))
                    update = arg;
                else
                    error('Update option must be a string: (''dynamic''|''static''|''scroll'')');
                end
            case 'units'
                warning('Units are set by the anchor system. This argument will be ignored');
            case 'parent'
                if (ishandle(arg) && ~exist('parent','var'))
                    parent = arg;
                end
            case 'titles'
                if (iscell(arg))
                    titleList = arg;
                else
                    error ('Titles argument must be a cell array of strings (Titles, {''t1'' ''t2'' ...}).');
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
if(~exist('titleList','var'))
    error ('Must specify a cell array of tab titles (Titles, {''t1'' ''t2'' ...}).');
elseif (isempty(titleList))
    error ('Cell array of titles must have at least one element (Titles, {''t1'' ''t2'' ...}).');
end


[TopContainer,handles]= anchoredPanel(handles,args{:},'parent',parent,'location',loc,'position',pos,'Update',update);
[content,handles]= anchoredPanel(handles,'parent',TopContainer,'Location','expand',...
    'position',[1 1 1 20]);
[tabBar,handles]= anchoredPanel(handles,'parent',TopContainer,'Location','top',...
    'position',[4 1 0 20]);

num = length(titleList);
width = 1/num;
position = 0;

tabHandleList = [];
textHandleList = [];
contentHandleList = [];

for i = 1:length(titleList)
    [p3,handles]= anchoredPanel(handles,'parent',content,'Location','expand',...
        'position',[0 0 0 0],'bordertype','line','Visible','on','highlightcolor',[175 175 175]./255);
    
    if i ~= length(titleList)
        offset = 0.01;
    else
        offset = 0;
    end
    title = titleList{i};
    % Had to change from outerPosition to Position for V2013b
    p1 = uipanel('units','normalized','position',...
        [position 0 width+offset 1],'parent',tabBar,'bordertype','line','highlightcolor',[175 175 175]./255,...
        'backgroundcolor',[240 240 240]./255,'borderwidth',1);
    position = position + width;
    p2 = uicontrol(p1,'style','text','String',title,'units','normalized',...
        'position',[0 0 1 1],'hittest','off','Enable','inactive');
    tabHandleList = [tabHandleList p1];
    textHandleList = [textHandleList p2];
    contentHandleList = [contentHandleList p3];
end

for i = 1:length(titleList)
    set(tabHandleList(i),'ButtonDownFcn',{@tabButton,handles.f,textHandleList(i),i,contentHandleList,tabHandleList,textHandleList});
end

tabButton(tabHandleList(1),'',handles.f,textHandleList(1),...
    1,contentHandleList,tabHandleList,textHandleList);

fh = contentHandleList;
% fh = fliplr(contentHandleList);

    function tabButton(src,~,hObject,text,index,contentList,tabList,textList)
        
        for a = 1:length(tabList)
            set(tabList(a),'BackgroundColor',low);
            set(textList(a),'BackgroundColor',low);
            set(contentList(a),'Visible','off');
        end
        set(src,'BackgroundColor',high);
        set(text,'BackgroundColor',high);
        set(contentList(index),'Visible','on');
        
        variableSizeManager(hObject);

        for a = 1:length(tabList)
            set(textList(a),'hittest','off','Enable','inactive')
        end
    end
end