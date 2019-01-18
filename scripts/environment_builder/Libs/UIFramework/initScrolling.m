function handles = initScrolling(handles,rst)
max = 0;
min = 0;
if (isfield(handles, 'anchors'))
    numScrolls = sum(cell2mat(strfind(fieldnames(handles),'ScrollPanel')));
    for i = 1:numScrolls
        numEl = sum(cell2mat(strfind(fieldnames(handles.anchors),'el')));
        for a = 1:numEl
            handle = handles.anchors.(['el' num2str(a)]);
            if (isfield(handle, 'sliderReference') && strcmpi(handle.sliderReference,['ScrollPanel' num2str(i)]))
                if(handles.(['ScrollPanel' num2str(i)]).update == 1)
                    handles.anchors.(['el' num2str(a)]).update = 2;
                end
                if handle.position(2) > max
                    max = handle.position(2) + handle.position(3);
                end
                if handle.position(2) < min
                    min = handle.position(2);
                end
            end
        end
        handles.(['ScrollPanel' num2str(i)]).height = max - min;
        if (rst == true)
            set(handles.(['ScrollPanel' num2str(i)]).slider,'Value', 1);
        end
        set(handles.(['ScrollPanel' num2str(i)]).slider,'Enable', 'off');
        addlistener(handles.(['ScrollPanel' num2str(i)]).slider,'Value',...
            'PreSet',@(~,~)slider(handles.(['ScrollPanel' num2str(i)]).slider,'slider',handles.f));

    end
%     numEl = sum(cell2mat(strfind(fieldnames(handles.anchors),'el')));
%     for i = 1:numEl
%         handles.anchors.(['el' num2str(a)])
%     end
end