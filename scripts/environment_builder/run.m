function external = run (varargin)
    close all;
    
    addpath(genpath('./'));
    
    % -- Init Function. Do not remove. Set name, menubarm, and numbertitle -- %
    handles = GUI_INIT('Environment Builder', 'none', 'off');
    set(handles.f, 'pointer', 'watch');
    drawnow;
    
    handles.model = 'ComponentTesting_MultiTarget';
    
    
    % -- Init Functions. Do not Modify, except start settings for GUI_INIT -- %
    [handles, external] = GUI_POPULATE(handles);
    handles = SET_CALLBACKS(handles,external);
    [handles, external] = INIT_VARS(handles,external);
    GUI_ACTIVATE(handles);
    if (~isempty(varargin) && ~isempty(varargin{1}))
        b31_loadConfig(external.figure,'init',external,varargin{1});
    end
    set(handles.f, 'pointer', 'arrow');
    drawnow;
end

function figDelete(~,~)
    %     close_system('ComponentTesting_MultiTarget',1);
end

function handles = GUI_INIT(name,menubar,numbertitle)
    handles.f = figure('Visible','off','menubar',menubar,'numbertitle',numbertitle,'units','pixels',...
        'name',name,'SizeChangedFcn',{@variableSizeManager},'WindowScrollWheelFcn',@slider,...
        'DeleteFcn',@figDelete,'tag','hObject');
    
    guidata(handles.f, handles);
end

function GUI_ACTIVATE(handles)
    handles = initScrolling(handles,true);
    guidata(handles.f, handles);
    variableSizeManager(handles.f,'init');
    set(handles.f,'Visible','on');
end

function [handles, external] = GUI_POPULATE(handles)
    external.figure = handles.f;
    
    % File Menu
    external.file = uimenu('label','File');
    external.file_saveConfig = uimenu(external.file,'label','Save Configuration','accelerator','s');
    external.file_loadConfig = uimenu(external.file,'label','Load Configuration','accelerator','o');
    external.file_quit = uimenu(external.file,'label','Quit','separator','on','accelerator','w'); 
    
    % Main Container
    [main, handles] = anchoredPanel(handles,'parent',handles.f,'location','expand','position',[0,0,0,0]);
    
    % Containers
    [containerRight, handles] = anchoredPanel(handles,'parent',main,'position',[2.5 5 2.5 200],'location','left');
    handles.containerRight = containerRight;
    [containerLeft, handles] = anchoredPanel(handles,'parent',main,'position',[205 0 0 0],...
        'location','Expand');

    % Sub Containers
    [mainSettings, handles] = scrollPane(handles,'parent',handles.containerRight,'title','Main Settings',...
        'position',[1 111 1 0],'location','expand','update','dynamic','clipping','on');
    
    % - Top Lefft (Scroll Panel)
    offset = 0;
    [~,handles] = anchoredElement(handles,'style','text','parent',mainSettings,'string',...
        'General Settings','location','top','position',[5 15 -2 20]);
    [external.s1, handles] = editBox(handles,'Title','Num. Bases','DefaultText','2','Location','top',...
        'Position',[5 (36 + offset) 0 20],'Ratios',[0.01 0.40 0.96],'Parent',mainSettings,'update','dynamic');
    [external.s2, handles] = editBox(handles,'Title','Num. Nodes','DefaultText','7','Location','top',...
        'Position',[5 (57 + offset) 0 20],'Ratios',[0.01 0.40 0.96],'Parent',mainSettings,'update','dynamic');
    [external.s3, handles] = editBox(handles,'Title','Num. Range','DefaultText','200','Location','top',...
        'Position',[5 (78 + offset) 0 20],'Ratios',[0.01 0.40 0.96],'Parent',mainSettings,'update','dynamic');
    
    offset = 108;
    [~,handles] = anchoredElement(handles,'style','text','parent',mainSettings,'string',...
        'Node Names','location','top','position',[5 (0 + offset) -2 20]);
    [external.s4,handles] = titleElement(handles,'style','popupmenu','Title','Node',...
        'string',{'(1) Base 1'},'Location','top','Position',[5 (21 + offset) -2 20],'Ratios',...
        [0.01 0.20 0.99],'Parent',mainSettings,'update','dynamic');
    [external.s5, handles] = editBox(handles,'Title','Name','DefaultText','Base 1','Location','top',...
        'Position',[5 (45 + offset) 0 20],'Ratios',[0.01 0.20 0.96],'Parent',mainSettings,'update','dynamic');
    
%     [external.s3, handles] = titleElement(handles,'Title','Swerling','Location','top',...
%         'Position',[5 78 0 20],'Ratios',[0.01 0.40 0.96],'Parent',mainSettings,'style','checkbox');
    
    % Bottom Left (I/O Options)
    %  - Pannels
    [runSettings, handles] = anchoredPanel(handles,'title','I/O Options',...
        'parent',handles.containerRight,'position',[1 0 0 111],'location',...
        'bottom','bordertype','etchedin','update','static');
    [savePanel, handles] = anchoredPanel(handles,...
        'parent',runSettings,'position',[1 50 2 20],'location',...
        'bottom','bordertype','none','update','static');
    [executePanel, handles] = anchoredPanel(handles,...
        'parent',runSettings,'position',[1 27 2 20],'location',...
        'bottom','bordertype','none','update','static');
    
    [external.i4, handles] = editBox(handles,'Title','Env. Name','DefaultText','env','Location','bottom',...
        'Position',[5 76 1 20],'Ratios',[0.01 0.30 0.99],'Parent',handles.containerRight,'update','dynamic');
    
    %  - Buttons
    external.i1 = uicontrol('style','pushbutton','units','normalized','position',[0.01 0.01 0.46 0.99],...
        'parent',savePanel,'string','Load Env');
    external.i2 = uicontrol('style','pushbutton','units','normalized','position',[0.50 0.01 0.46 0.99],...
        'parent',savePanel,'string','Save Env');
    external.i3 = uicontrol('style','pushbutton','units','normalized','position',[0.01 0.01 0.955 0.99],...
        'parent',executePanel,'string','Generate Measurements');
    
    %  - Loading Bar
    [loadBar, handles] = anchoredPanel(handles,'parent',runSettings,'position',[5.5 5 -1 20],...
        'location','bottom','bordertype','line','highlightcolor',[175 175 175]./255,'update','static');
    
    external.wBar = uiwaitbar(loadBar,[0 0 1 1]);
    uiwaitbar(external.wBar,0,'set');
    handles.wbar = external.wBar;
    set (external.wBar,'tag','loadBar');
    
    % Left (Axis Region)
    [external.handleList, handles] = anchoredContentPanel(handles,'location','expand','position',[5 6 0 4],...
        'parent',containerLeft,'titles',{'Point Positions','Range Assessment'});

    ax1 = axes('parent',external.handleList(1),'units','normalized','outerposition',[0 -0.02 0.96 1],'Tag','axes_pos');
    ax2 = axes('parent',external.handleList(2),'units','normalized','outerposition',[0 -0.02 0.96 1],'Tag','axes_range');
    
    external.ax1 = ax1;
    external.ax2 = ax2;
    
        
    external.xmax = 700;
    external.ymax = 700;
    external.xmin = 0;
    external.ymin = 0;
    
    external.nodes = Nodes();
    
    numBase = str2num(get(external.s1,'String'));
    numNode = str2num(get(external.s2,'String'));
    x = linspace(external.xmin + (external.xmax/10),external.xmax - (external.xmax/10),numNode + numBase);
    y = linspace(external.ymin + (external.ymax/10),external.ymax - (external.ymax/10),numNode + numBase);
    
    for i = 1:1:(numBase+numNode)
        if (i > numBase)
            external.nodes.addNode(x(i),y(i),['Node ' num2str(i - numBase)]);
        else
            external.nodes.addBase(x(i),y(i),['Base ' num2str(i)]);
        end
    end
    
    external.landscape = csvread('landscape.csv',1,0);
    
    external.model = handles.model;
end



% Set Callbacks function: Use this function to set all of the action
% (non system) callbacks [eg: buttons, edit box entry, etc...].
% Callback functions set here have access to the full external variable
% if set as follows:
%   set(external.button,'Callback',{@button_callback,external});
function handles = SET_CALLBACKS(handles,external)
    
    set(external.file_quit,'Callback',{@(~,~)close(external.figure)});
    set(external.i3,'Callback',{@generateMeasurements,external});
    
    set(external.s1, 'Callback',{@num_check,2,handles,external});
    set(external.s2, 'Callback',{@num_check,7,handles,external});
    set(external.s3, 'Callback',{@num_check,7,handles,external});
    
    set(external.s4, 'Callback',{@update_names_list,handles,external});
    set(external.s5, 'Callback',{@update_names_data,handles,external});
%     set(external.file_loadConfig,'Callback',{@(~,~)close(external.figure)});
    
end

function update_names_data(src,val,handles,external)
    idx = get(external.s4,'Value');
    
    % If we are now selected on a spot that should not exist, do not bother
    % trying to update the node or base list data
    if (idx <= external.nodes.numBases() + external.nodes.numNodes())
    
        name = get(external.s5,'String');

        if (idx > external.nodes.numBases())
            external.nodes.nodeList{idx - external.nodes.numBases()}.name = name;
        else
            external.nodes.baseList{idx}.name = name;
        end
    end
    
    update_names_list(src,val,handles,external);
end

function update_names_list(src,~,handles,external)
    idx = get(external.s4,'Value');
    if (idx > external.nodes.numBases() + external.nodes.numNodes())
        idx = external.nodes.numBases() + external.nodes.numNodes();
    end
    
    if (idx > 0)
    
        external.s4.String = {};
        for i = 1:1:(external.nodes.numBases() + external.nodes.numNodes())
            if (i > external.nodes.numBases())
                external.s4.String{end+1} = ['(' num2str(i) ') ' external.nodes.nodeList{i - external.nodes.numBases()}.name];
            else
                external.s4.String{end+1} = ['(' num2str(i) ') ' external.nodes.baseList{i}.name];
            end
        end
        if (idx > external.nodes.numBases())
            external.s5.String = external.nodes.nodeList{idx - external.nodes.numBases()}.name;
        else
            external.s5.String = external.nodes.baseList{idx}.name;
        end
        external.s4.Value = idx;
    else 
        external.s4.String = {''};
        external.s4.Value = 1;
        external.s5.String = '';
    end
    
end

function num_check(src,val,default,handles,external)
    value = real(str2num(get(src,'String'))); %#ok;
    
    if (length(value) ~= 1 || any(isempty(value)) || any(isnan(value)) || value < 0)
        set(src,'String',num2str(default));
    else
        set(src,'String',num2str(value));
        setPlots(handles,external);
    end
    
    update_names_list(src,val,handles,external);
end

function [handles, external] = INIT_VARS(handles,external)
    
    setPlots(handles,external);
    update_names_data(0,0,handles,external);
    
    % Dragging Plot:
end

function setPlots(handles, external)
    % collect information
    
    numBase = str2num(get(external.s1,'String'));
    numNode = str2num(get(external.s2,'String'));
    
    while(external.nodes.numNodes() > numNode)
        external.nodes.removeNode()
    end
    
    while(external.nodes.numNodes() < numNode)
        external.nodes.addNode(50, 50, ['Node ' num2str(external.nodes.numNodes()+1)]);
    end
    
    while(external.nodes.numBases() > numBase)
        external.nodes.removeBase()
    end
    
    while(external.nodes.numBases() < numBase)
        external.nodes.addBase(50, 100, ['Base ' num2str(external.nodes.numBases()+1)]);
    end
    
    x = []; y = [];

    for i = 1:1:(external.nodes.numBases()+external.nodes.numNodes())
        if (i > external.nodes.numBases()) 
           x(end+1) = external.nodes.nodeList{i - external.nodes.numBases()}.x; 
           y(end+1) = external.nodes.nodeList{i - external.nodes.numBases()}.y;
        else
           x(end+1) = external.nodes.baseList{i}.x; 
           y(end+1) = external.nodes.baseList{i}.y;
        end
    end

    cla(external.ax1);
    cla(external.ax2);
    
    % Add the landscape to plot 1
    fill(external.ax1, external.landscape(:,1),external.landscape(:,2),'g','LineStyle','--',...
    'FaceAlpha',0.1,'EdgeColor','g','LineWidth',2);
    
    % Add the main scatter plot to plot 1
    hold(external.ax1, 'on');
    h = scatter(external.ax1, x,y,100, 'filled','hittest','on','buttondownfcn',{@clickmarker, handles,external});
    hold(external.ax1, 'off');

    % Change color of base stations
    c = h.CData;
    c = repmat(c,[numNode+numBase 1]);
    c(1:numBase,:) = repmat([0 0 1], [numBase 1]);
    c(numBase+1:end,:) = repmat([1 0 0], [numNode 1]);
    h.CData = c;
    % /Position Plot
    
    % Range Plot
    
    range = str2num(get(external.s3,'String'));
    hold(external.ax2, 'on');
    for i = 1:1:length(x)
        circle(external.ax2,x(i),y(i),range);
    end
    
    h = scatter(external.ax2, x,y,100,'filled');
    hold(external.ax2, 'off');

    
    % Change color of base stations
    c = h.CData;
    c = repmat(c,[numNode+numBase 1]);
    c(1:numBase,:) = repmat([0 0 1], [numBase 1]);
    c(numBase+1:end,:) = repmat([1 0 0], [numNode 1]);
    h.CData = c;
    % / Range Plot

    set(external.ax1,'XMinorGrid','on', 'XGrid','on','YMinorGrid','on', 'YGrid','on', 'Ydir', 'reverse');
    set(external.ax2,'XMinorGrid','on', 'XGrid','on','YMinorGrid','on', 'YGrid','on', 'Ydir', 'reverse');
    xlabel(external.ax1,'X Position (ft)');
    ylabel(external.ax1,'Y Position (ft)');
    xlabel(external.ax2,'X Position (ft))');
    ylabel(external.ax2,'Y Position (ft)');
    
    title(external.ax1,'Node Position Graph');
    title(external.ax2,'Range Assessment Graph');
    
    axis(external.ax1,'equal');
    axis(external.ax2,'equal');
    
    axis(external.ax1, [external.xmin external.xmax external.ymin external.ymax]);
    axis(external.ax2, [external.xmin external.xmax external.ymin external.ymax]);
end

% Draging Functionality
function clickmarker(src,ev,handles,external)
    set(ancestor(src,'figure'),'windowbuttonmotionfcn',{@dragmarker,src,handles,external})
    set(ancestor(src,'figure'),'windowbuttonupfcn',{@stopdragging,external})
end

function dragmarker(fig,ev,src,handles,external)

    %get current axes and coords
    h1=external.ax1;
    coords=get(h1,'currentpoint');

    %get all x and y data 
    x=h1.Children(1).XData;
    y=h1.Children(1).YData;

    %check which data point has the smallest distance to the dragged point
    x_diff=abs(x-coords(1,1,1));
    y_diff=abs(y-coords(1,2,1));
    [value index]=min(x_diff+y_diff);

    %create new x and y data and exchange coords for the dragged point
    x_new=x;
    y_new=y;
    x_new(index)=coords(1,1,1);
    y_new(index)=coords(1,2,1);

    x_new(x_new>external.xmax) = external.xmax;
    x_new(x_new<external.xmin) = external.xmin;
    y_new(y_new>external.ymax) = external.ymax;
    y_new(y_new<external.ymin) = external.ymin;

    %update plot
    set(src,'xdata',x_new,'ydata',y_new);
    
%     for i = 1:1:(external.nodes.numBases()+external.nodes.numNodes())
%         if (i > external.nodes.numBases()) 
%            external.nodes.nodeList{i - external.nodes.numBases()}.x = x_new(i); 
%            external.nodes.nodeList{i - external.nodes.numBases()}.y = y_new(i);
%         else
%            external.nodes.baseList{i}.x = x_new(i); 
%            external.nodes.baseList{i}.y = y_new(i);
%         end
%     end
%     setPlots(handles, external)
end

function stopdragging(fig,ev,external)
    set(fig,'windowbuttonmotionfcn','')
    set(fig,'windowbuttonupfcn','')
    
    % Copy over the data from ax1 to ax2
    external.ax2.Children(1).XData=external.ax1.Children(1).XData;
    external.ax2.Children(1).YData=external.ax1.Children(1).YData;
    
    % Update the range circles on the second plot
    r = str2num(get(external.s3,'String'));
    for i = 1:1:length(external.ax1.Children(1).XData)
        d = r*2;
        px = external.ax1.Children(1).XData(i)-r;
        py = external.ax1.Children(1).YData(i)-r;
        
        external.ax2.Children(i+1).Position = [px py d d];
    end
    
    % Store the new locations back into the nodes list
    for i = 1:1:(external.nodes.numBases()+external.nodes.numNodes())
        if (i > external.nodes.numBases()) 
           external.nodes.nodeList{i - external.nodes.numBases()}.x = external.ax1.Children(1).XData(i); 
           external.nodes.nodeList{i - external.nodes.numBases()}.y = external.ax1.Children(1).YData(i);
        else
           external.nodes.baseList{i}.x = external.ax1.Children(1).XData(i); 
           external.nodes.baseList{i}.y = external.ax1.Children(1).YData(i);
        end
    end
    
end
% / Dragging Functionality

function generateMeasurements(~,~,external)
    
    x = external.ax1.Children(1).XData;
    y = external.ax1.Children(1).YData;
    range = str2num(get(external.s3,'String'));
    
    names = {'Base1','Base2','Node1','Node2','Node3','Node4','Node5','Node6','Node7'};
    base = [1,1,0,0,0,0,0,0,0];
    
    numEl = length(x);
   
    fdefs = fopen([get(external.i4,'String') '.def'],'w');
    fprintf(fdefs,'NodeID,Name,Is Base?,X coordinate,Y coordinate\n');
    for i = 1:1:numEl
        fprintf(fdefs,'%d,%s,%d,%d,%d\n',i,names{i},base(i),x(i),y(i));
    end
    fclose(fdefs);
    
    
    fdat = fopen([get(external.i4,'String') '.dat'],'w');
    fprintf(fdat,'NodeA,NodeA,Distance\n');

    count = 1;
    for a = 1:1:numEl
        for b = 1:1:numEl
            if (a == b)
                continue;
            end
            x1 = x(a);
            x2 = x(b);
            y1 = y(a);
            y2 = y(b);
            dist = sqrt((x2 - x1) .^2 + (y2 - y1) .^2);
            
            if (dist > range)
                continue;
            end
            
            % Write to the file
            fprintf(fdat,'%d,%d,%d\n',a,b,dist);
            
            % Update the loading bar
            uiwaitbar(external.wBar,count/(numEl*(numEl-1)),'set');
            count = count + 1;
        end
    end
    
    fclose(fdat);
    
    uiwaitbar(external.wBar,1,'set')
    
    % NodeA,NodeB,Distance
    
    
end
    
% x = 0:30:300;
% y = x;
% dragpoints(x,y);