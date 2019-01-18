function external = shell
    close all;
    
    % -- Init Function. Do not remove. Set name, menubarm, and numbertitle -- %
    handles = GUI_INIT('Main GUI', 'none', 'off');
    
    % -- Init Functions. Do not Modify.                                    -- %
    external.figure = handles.f;
    [handles, external] = GUI_POPULATE(handles,external);
    [handles, external] = SET_CALLBACKS(handles,external);
    [handles, external] = INIT_VARS(handles,external);
    GUI_ACTIVATE(handles);
    external.func = @test;
end

% Function is called when the figure is deleted
function figDelete(~,~)
end

% Init function for the GUI. If you do not want center mouse wheel scroll
% support, remove the WindowScrollWheelFcn callback.
function handles = GUI_INIT(name,menubar,numbertitle)
    handles.f = figure('Visible','off','menubar',menubar,'numbertitle',numbertitle,'units','pixels',...
        'name',name,'SizeChangedFcn',{@variableSizeManager},'WindowScrollWheelFcn',@slider,...
        'DeleteFcn',@figDelete,'tag','hObject');
    guidata(handles.f, handles);
end

% Activate function. Draws the gui, sets anchors, and makes it visible for
% the user. This should be the last thing that is run before returning the
% external struct to the user. If scrolling is not used at all, comment out
% the initScrolling line
function GUI_ACTIVATE(handles)
    handles = initScrolling(handles,true);
    guidata(handles.f, handles);
    variableSizeManager(handles.f,'init');
    handles.f.Visible = 'on';
end

% ------                          -------                          ------ %

% Populate Function: Sets the layout for the GUI. Set the content of the
% gui here. Handles is the internal handle container, external is the
% usable container for external control and callback functions. Do not set
% callbacks here.
function [handles, external] = GUI_POPULATE(handles,external)
    
    % Containers
    [containerRight, handles] = anchoredPanel(handles,'parent',handles.f,'position',[5 5 0 200],'location','left');
    
    % Elements
    [external.b1, handles] = editBox(handles,'Title','Init Range Error','DefaultText','50','Location','center',...
        'Position',[150 20 20 20],'Ratios',[0.01 0.53 0.99],'Parent',containerRight,'update','dynamic');
end

% Set Callbacks function: Use this function to set all of the action
% (non system) callbacks [eg: buttons, edit box entry, etc...].
% Callback functions set here have access to the full external variable.
% While this method returns both the handles and external structures, these
% do not need to be modified to set callbacks so it is unwise to change
% them.
% if set as follows:
%   set(external.button,'Callback',{@button_callback,external});
function [handles, external] = SET_CALLBACKS(handles,external)
    set(external.b1, 'Callback',{@b1_check,0});
end

% Function INITVARS: Use this method to run any pre-render commands. This
% can include callbacks (because this method us run after the SET_CALLBACKS
% method). Note that this method returns both the handles and external
% structures so both can be set from within this method
function [handles, external] = INIT_VARS(handles,external)
    handles.test = 5;
    external.test = handles.test;
end

% Function Callbacks: Use this space to list all of the GUI Callback
% functions. Functions here have access to the external variable if set
% as follows:
%   function button_callback(src,event,external), end
function b1_check(src,~,default)
    value = real(str2num(src.String)); %#ok;
    if (length(value) ~= 1 || any(isempty(value)) || any(isnan(value)))
        src.String = num2str(default);
    else
        src.String = num2str(value);
    end
end

function b = test (a)
    b = a.*2;
end
