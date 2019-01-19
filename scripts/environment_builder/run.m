function external = run (varargin)
    close all;
    
    % Add all of the lib items to the path
    addpath(genpath('./'));
    
    % -- Init Function. Do not remove. Set name, menubarm, and numbertitle -- %
    handles = GUI_INIT('Environment Builder', 'none', 'off');
    set(handles.f, 'pointer', 'watch');
    drawnow;
    
    
    % -- Init Functions. Do not Modify, except start settings for GUI_INIT -- %
    [handles, external] = GUI_POPULATE(handles);
    handles = SET_CALLBACKS(handles,external);
    [handles, external] = INIT_VARS(handles,external);
    GUI_ACTIVATE(handles);
    if (~isempty(varargin) && ~isempty(varargin{1}))
        % b31_loadConfig(external.figure,'init',external,varargin{1});
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
    [external.s3, handles] = editBox(handles,'Title','Node Range','DefaultText','200','Location','top',...
        'Position',[5 (78 + offset) 0 20],'Ratios',[0.01 0.40 0.96],'Parent',mainSettings,'update','dynamic');
    
    offset = 108;
    [~,handles] = anchoredElement(handles,'style','text','parent',mainSettings,'string',...
        'Node Names','location','top','position',[5 (0 + offset) -2 20]);
    [external.s4,handles] = titleElement(handles,'style','popupmenu','Title','Node',...
        'string',{'(1) Base 1'},'Location','top','Position',[5 (21 + offset) -2 20],'Ratios',...
        [0.01 0.20 0.99],'Parent',mainSettings,'update','dynamic');
    [external.s5, handles] = editBox(handles,'Title','Name','DefaultText','Base 1','Location','top',...
        'Position',[5 (45 + offset) 0 20],'Ratios',[0.01 0.20 0.96],'Parent',mainSettings,'update','dynamic');
    
    offset = 180;
    [~,handles] = anchoredElement(handles,'style','text','parent',mainSettings,'string',...
        'Measurement Settings','location','top','position',[5 (0 + offset) -2 20]);
%     [external.s6,handles] = titleElement(handles,'style','popupmenu','Title','Node',...
%         'string',{'(1) Base 1'},'Location','top','Position',[5 (21 + offset) -2 20],'Ratios',...
%         [0.01 0.20 0.99],'Parent',mainSettings,'update','dynamic');
    [external.s6, handles] = editBox(handles,'Title','Meas. Fluctuation','DefaultText','1','Location','top',...
        'Position',[5 (21 + offset) 0 20],'Ratios',[0.01 0.50 0.96],'Parent',mainSettings,'update','dynamic');
    [external.s7, handles] = editBox(handles,'Title','Range Fluctuation','DefaultText','30','Location','top',...
        'Position',[5 (42 + offset) 0 20],'Ratios',[0.01 0.50 0.96],'Parent',mainSettings,'update','dynamic');
    [external.s8, handles] = editBox(handles,'Title','Maximum Error','DefaultText','1','Location','top',...
        'Position',[5 (63 + offset) 0 20],'Ratios',[0.01 0.50 0.96],'Parent',mainSettings,'update','dynamic');
    [external.s9, handles] = editBox(handles,'Title','Drop Probability','DefaultText','0','Location','top',...
        'Position',[5 (84 + offset) 0 20],'Ratios',[0.01 0.50 0.96],'Parent',mainSettings,'update','dynamic');
    
    offset = 295;
    [~,handles] = anchoredElement(handles,'style','text','parent',mainSettings,'string',...
        'View Settings','location','top','position',[5 (0 + offset) -2 20]);
    [external.s10, handles] = titleElement(handles,'Title','Show Text Names','Location','top',...
        'Position',[5 (18 + offset) 0 20],'Value',1,'Ratios',[0.01 0.65 0.99],'Parent',mainSettings,'style','checkbox');
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
    
        
    external.xmax = 2000;
    external.ymax = 2000;
    external.xmin = 0;
    external.ymin = 0;
    external.storePath = '../../datasets/';
    
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
    
    external.landscape = csvread([external.storePath 'landscape.csv'],1,0);
end



% Set Callbacks function: Use this function to set all of the action
% (non system) callbacks [eg: buttons, edit box entry, etc...].
% Callback functions set here have access to the full external variable
% if set as follows:
%   set(external.button,'Callback',{@button_callback,external});
function handles = SET_CALLBACKS(handles,external)
    
    set(external.file_quit,'Callback',{@(~,~)close(external.figure)});
    set(external.i3,'Callback',{@generateMeasurements,external});
    set(external.i4,'Callback',{@check_text,'env',handles,external});
    
    set(external.s1, 'Callback',{@num_check,2,handles,external});
    set(external.s2, 'Callback',{@num_check,7,handles,external});
    set(external.s3, 'Callback',{@num_check,7,handles,external});
    
    set(external.s4, 'Callback',{@update_names_list,handles,external});
    set(external.s5, 'Callback',{@update_names_data,handles,external});
    
    set(external.s6, 'Callback',{@check_content,1,handles,external});
    set(external.s7, 'Callback',{@check_content,30,handles,external});
    set(external.s8, 'Callback',{@check_content,1,handles,external});
    set(external.s9, 'Callback',{@check_content,0,handles,external});
    
    set(external.s10, 'Callback',{@callback_set_plots,handles,external});
    
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
    
    setPlots(handles, external);
    
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

function callback_set_plots(~,~,handles,external)
    setPlots(handles, external);
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
    
    x = []; y = []; names = {};

    for i = 1:1:(external.nodes.numBases()+external.nodes.numNodes())
        if (i > external.nodes.numBases()) 
           x(end+1) = external.nodes.nodeList{i - external.nodes.numBases()}.x; 
           y(end+1) = external.nodes.nodeList{i - external.nodes.numBases()}.y;
           names{end+1} = external.nodes.nodeList{i - external.nodes.numBases()}.name;
        else
           x(end+1) = external.nodes.baseList{i}.x; 
           y(end+1) = external.nodes.baseList{i}.y;
           names{end+1} = external.nodes.baseList{i}.name;
        end
    end

    cla(external.ax1);
    cla(external.ax2);
    
    % Add the landscape to plot 1
    fill(external.ax1, external.landscape(:,1),external.landscape(:,2),'g','LineStyle','-',...
    'FaceAlpha',0.1,'EdgeColor','g','LineWidth',0.2);
    
    % Add the main scatter plot to plot 1
    hold(external.ax1, 'on');
    
    if (external.s10.Value)
        for i = 1:1:length(x)
            text(external.ax1,x(i)+20,y(i),names{i});
        end
    end
    h = scatter(external.ax1, x,y,100, 'filled','hittest','on','ButtonDownFcn',{@clickmarker,external.ax1,handles,external});
    hold(external.ax1, 'off');

    % Change color of base stations
    c = h.CData;
    c = repmat(c,[numNode+numBase 1]);
    c(1:numBase,:) = repmat([0 0 1], [numBase 1]);
    c(numBase+1:end,:) = repmat([1 0 0], [numNode 1]);
    h.CData = c;
    % /Position Plot
    
    fill(external.ax2, external.landscape(:,1),external.landscape(:,2),'g','LineStyle','-',...
    'FaceAlpha',0.1,'EdgeColor','g','LineWidth',0.2);
    
    % Text Labels
    for i = 1:1:length(x)
        if (external.s10.Value)
            text(external.ax2,x(i)+20,y(i),names{i});
        end
    end
    % Range Plot
    range = str2num(get(external.s3,'String'));
    hold(external.ax2, 'on');
    for i = 1:1:length(x)
        circle(external.ax2,x(i),y(i),range);
    end
    h = scatter(external.ax2, x,y,100,'filled','hittest','on','ButtonDownFcn',{@clickmarker,external.ax2,handles,external});
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
    
    title(external.ax1,'Node Position Graph (Drag Dots to Change Position)');
    title(external.ax2,'Range Assessment Graph');
    
    axis(external.ax1,'equal');
    axis(external.ax2,'equal');
    
    axis(external.ax1, [external.xmin external.xmax external.ymin external.ymax]);
    axis(external.ax2, [external.xmin external.xmax external.ymin external.ymax]);
end

% Draging Functionality
function clickmarker(src,ev,ax,handles,external)
    %get current axes and coords
    h1=ax; %external.ax1;
    coords=get(h1,'currentpoint');
    
    %get all x and y data 
    x=h1.Children(1).XData;
    y=h1.Children(1).YData;

    %check which data point has the smallest distance to the dragged point
    x_diff=abs(x-coords(1,1,1));
    y_diff=abs(y-coords(1,2,1));
    [value, index]=min(x_diff+y_diff);
    
    
    set(ancestor(src,'figure'),'windowbuttonmotionfcn',{@dragmarker,src,ax,index,handles,external})
    set(ancestor(src,'figure'),'windowbuttonupfcn',{@stopdragging,ax,handles,external})
end

function dragmarker(fig,ev,src,ax,index,handles,external)

    %get current axes and coords
    h1=ax; %external.ax1;
    coords=get(h1,'currentpoint');
% 
%     %get all x and y data 
    x=h1.Children(1).XData;
    y=h1.Children(1).YData;
% 
%     %check which data point has the smallest distance to the dragged point
%     x_diff=abs(x-coords(1,1,1));
%     y_diff=abs(y-coords(1,2,1));
%     [value index]=min(x_diff+y_diff);

    %create new x and y data and exchange coords for the dragged point
    x_new=x;
    y_new=y;
    x_new(index)=coords(1,1,1);
    y_new(index)=coords(1,2,1);

    x_new(x_new>external.xmax - 10) = external.xmax - 10;
    x_new(x_new<external.xmin + 10) = external.xmin + 10;
    y_new(y_new>external.ymax - 10) = external.ymax - 10;
    y_new(y_new<external.ymin + 10) = external.ymin + 10;

    %update plot
    set(src,'xdata',x_new,'ydata',y_new);
    
    % Also move visual elements around as well
    % First grab some flags
    numelems = external.nodes.numNodes() + external.nodes.numBases();
    doText = external.s10.Value;
    % Check which axis we are looking at
    if (ax == external.ax1)
        % Sex Axis 1 text
        if (doText)
            ax.Children(numelems - index + 2).Position = [x_new(index)+20,y_new(index),0];
        end
    else
        % Grab the node range 
        r = str2num(get(external.s3,'String'));
        % Set Axis 2 text
        if (doText)
           ax.Children(numelems*2+2 - index).Position = [x_new(index)+20,y_new(index),0];
        end
        
        % Set Axis 2 range circle
        d = r*2;
        px = x_new(index)-r;
        py = y_new(index)-r;
        ax.Children(numelems - index + 2).Position = [px py d d];
    end

    
%     for i = 1:1:(external.nodes.numBases()+external.nodes.numNodes())
%         if (i > external.nodes.numBases()) 
%            external.nodes.nodeList{i - external.nodes.numBases()}.x = x_new(i); 
%            external.nodes.nodeList{i - external.nodes.numBases()}.y = y_new(i);
%         else
%            external.nodes.baseList{i}.x = x_new(i); 
%            external.nodes.baseList{i}.y = y_new(i);
%         end
%     end
%     setPlots(handles, external);
end

function check_content(src,~,default,~,~) 
    value = real(str2num(get(src,'String'))); %#ok;
    
    if (length(value) ~= 1 || any(isempty(value)) || any(isnan(value)) || value < 0)
        set(src,'String',num2str(default));
    else
        set(src,'String',num2str(value));
    end
end

function check_text (src,~,default,~,~) 
    if ~isempty(regexp(get(src,'String'), '[/\*:?"<>|]', 'once'))
        set(src,'String',default);
    end
end

function stopdragging(fig,ev,ax,handles,external)
    set(fig,'windowbuttonmotionfcn','')
    set(fig,'windowbuttonupfcn','')
    
    
    % Copy data between the axes
    if (ax == external.ax1)
        % Copy over the data from ax1 to ax2
        external.ax2.Children(1).XData=external.ax1.Children(1).XData;
        external.ax2.Children(1).YData=external.ax1.Children(1).YData;
    else
        % Copy over the data from ax2 to ax1
        external.ax1.Children(1).XData=external.ax2.Children(1).XData;
        external.ax1.Children(1).YData=external.ax2.Children(1).YData;
    end
    
    % Update the range circles on the second plot
%     r = str2num(get(external.s3,'String'));
%     for i = 1:1:length(external.ax1.Children(1).XData)
%         d = r*2;
%         px = external.ax1.Children(1).XData(i)-r;
%         py = external.ax1.Children(1).YData(i)-r;
%         
%         external.ax2.Children(i+1).Position = [px py d d];
%     end
    
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
    setPlots(handles, external);
end
% / Dragging Functionality

function generateMeasurements(~,~,external)
    
    x = external.ax1.Children(1).XData;
    y = external.ax1.Children(1).YData;
    range = str2num(get(external.s3,'String'));

   
    fdefs = fopen([external.storePath get(external.i4,'String') '.def'],'w');
    fprintf(fdefs,'NodeID,Name,Is Base?,X coordinate,Y coordinate\n');
    
    nodes = external.nodes.getAll();
    numEl = length(nodes);
    
    for i = 1:1:length(nodes)
        node = nodes{i};
        fprintf(fdefs,'%d,%s,%d,%d,%d\n',i,...
            node.name,node.isBase,node.x,node.y);
    end
    fclose(fdefs);
    
    
    fdat = fopen([external.storePath get(external.i4,'String') '.dat'],'w');
    fprintf(fdat,'NodeA,NodeA,Distance\n');
    
    distSd = external.s6.Value;
    rangeSd = external.s7.Value;
    maxErr = external.s8.Value;
    dropProb = external.s9.Value;

    count = 1;
    for a = 1:1:numEl
        nodeA = nodes{a};
        for b = 1:1:numEl
            nodeB = nodes{b};
            if (a == b || rand() < dropProb)
                continue;
            end
            x1 = nodeA.x;
            y1 = nodeA.y;
            x2 = nodeB.x;
            y2 = nodeB.y;
            dist = sqrt((x2 - x1) .^2 + (y2 - y1) .^2);
            
            % Factor in range fluctuation using a normal dist
            % rangeOffset = normrnd(0,rangeSd);
            rangeOffset = randn(1) * rangeSd + 0;
            if (dist > range + rangeOffset)
                continue;
            end
            
            % distOffset = normrnd(0,distSd);
            distOffset = randn(1) * distSd + 0;
            distVal = dist+distOffset;
            
            if (distVal - dist > maxErr)
                distVal = dist + maxErr;
            elseif (distVal - dist < -maxErr)
                distVal = dist - maxErr;
            end

            % Write to the file
            fprintf(fdat,'%d,%d,%d\n',a,b,distVal);
            
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