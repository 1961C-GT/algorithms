function slider(src,event,hObject)
% slider  Callback for controlling scroll bars.
% Usage (in the main figure)
%   f = figure(...,...,'WindowScrollWheelFcn',@slider);
%
% This method controls scrolling for the elements on the screen. It only
% allows the center scroll wheel to control the first scroll pane that was
% placed.
%
if(~exist('hObject','var'))
    
    hObject = src;
    handles = guidata(hObject);
    
    % Itterate through all of the scroll panels in the GUI
    
    for i = 1:sum(cell2mat(strfind(fieldnames(handles),'ScrollPanel')))
        % Get the mouse, scroll panel, and figure positions
        mpos = get(0,'PointerLocation');
        ppos = get(handles.(['ScrollPanel' num2str(i)]).panel,'Position');
        fpos = get(src,'Position');
        
        % The figure position tells where the bottom left corner of the window
        % is and the panel position is relative to the bottom left corner of
        % the window. Add them to get the absolute starting position of the
        % scroll panel
        loc = [fpos(1) + ppos(1) fpos(2) + ppos(2)];
        
        % Check that the mouse is over the scroll panel
        if (mpos(1) > loc(1) && mpos(1) < loc(1) + ppos(3) ...
                && mpos(2) > loc(2) && mpos(2) < loc(2) + ppos(4))
            
            % Move the scroll panel accordingly
            slid = handles.(['ScrollPanel' num2str(i)]).slider;
            if (strcmpi(get(slid,'Enable'),'on'))
                if isunix
                    set(slid,'Value',get(slid,'Value') - event.VerticalScrollCount/25);
                end
                %                 disp([num2str(event.VerticalScrollCount) ' ' num2str(event.VerticalScrollAmount) ' ' datestr(now, 'mm:ss:FFF')]);
                if (get(slid,'Value') > 1)
                    set(slid,'Value',1);
                elseif (get(slid,'Value') < 0)
                    set(slid,'Value',0);
                end
            end
        end
    end
end
handles = guidata(hObject);
handles.scrollupdate = 1;
guidata(src,handles);
variableSizeManager(hObject,event);
end