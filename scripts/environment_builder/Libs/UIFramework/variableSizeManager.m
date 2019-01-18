% variableSizeMananger  Callback function for running the anchored system
% Required usage:
%        handles.f = figure('SizeChangedFcn',{@variableSizeManager});
%        guidata(handles.f, handles);
%        % populate GUI here
%
% Recommended usage:
%        handles.f = figure('Visible','off','SizeChangedFcn',{@variableSizeManager});
%        guidata(handles.f, handles);
%        % populate GUI here
%        guidata(handles.f, handles);
%        variableSizeManager(handles.f,'init');
%        handles.f.Visible = 'on';
%
% Handles Structure:
%        handles
%            - f : Main figure handle
%            - anchors
%                  - el1
%                        - handle : handle to anchored object
%                        - pos    : anchored position vector
%                        - loc    : string location scheme
%
% Location List : Position Vector Contents
%   - Left      : [vert pad, off from left wall, vert off from center, fixed
%                  width]
%   - Right     : [vert pad, off from right wall, vert off from center, fixed
%                  width]
%   - Center    : [fixed width, fixed height, horiz off center, vert off
%                  center]
%   - Top       : [horiz pad, off from top wall, horiz off center, fixed
%                  height]
%   - Bottom    : [horiz pad, off from bot wall, horiz off center, fixed
%                  height]
%   - expand    : [off from left wall, off from bottom wall, off from right
%                  wall, off from top wall]
%
% Update Options: Scheme
%   0    :   Dynamic Update (default option)
%   1    :   Static Update (Only first draw). For this to increase
%            speed, all children must also be set to a static update.
%   2    :   Scroll (used only for elements in a scroll panel that is a
%            static size, either 'update static' or anchored to a fixed
%            size). Children of a static scrollpanel are automatically set
%            to the Scroll update scheme.
%
%   See also anchoredElement, variableSize.
function variableSizeManager(src,~)
    
    fig = src;
    th = findall(fig,'tag','bannerText');
    if ~isempty(th)
        ss = get(0,'screensize');
        figUnits = get(fig,'units');
        set(fig,'units','pixels');
        figPos = get(fig,'position');
        ud = get(th,'userdata');
        
        % first, check for mix and max limits
        if isfield(ud,'limits')
            % limits are defined in pixels as
            % [xMin xMax yMin yMax]
            lim = ud.limits;
            figPos(3) = max(figPos(3),lim(1));
            figPos(3) = min(figPos(3),lim(2));
            figPos(4) = max(figPos(4),lim(3));
            figPos(4) = min(figPos(4),lim(4));
            % Check for moving the figure of the top of the screen
            figPos(2) = min(figPos(2),ss(4) - 70 - figPos(4));
%             set(fig,'position',figPos)
        end
        
%         fprintf('FigPos in resize is [%i %i %i %i]\n',figPos);
        figH = figPos(4);
        for k=1:length(ud.handlesAtTop)
            curH    = ud.handlesAtTop(k);
            unitStr = get(curH,'units');
            set(curH, 'units','pixels');
            p = get(curH,'position');
            yPos = figH-ud.pixelsFromTop(k);
            if yPos < 1, yPos = 1; end
            set(curH,'position',[p(1) yPos p(3:end)]);
            set(curH,'units',unitStr);
        end
        set(fig,'units',figUnits)
    end
    
    handles = guidata(src);
    if(exist('minSize','var'))
        set(src, 'position', max([0 0 minSize], src.Position))
    end
    if (isfield(handles, 'anchors'))
        names = fieldnames(handles.anchors);
        for i = 1:length(names)
            el = handles.anchors.(names{i});
            update = el.update;
            if (update == -1 || strcmpi(get(el.handle,'Visible'),'off'))
                continue;
            end
            if (isfield(el, 'sliderReference') && isfield(handles, el.sliderReference));% && (~isfield(handles, 'scrollupdate') || handles.scrollupdate == 1))
                slide = get(handles.(el.sliderReference).slider,'Value');
                tmp = get(handles.(el.sliderReference).panel,'Position');
                windowHeight = tmp(4);
                paneHeight = handles.(el.sliderReference).height+25;
                scrollLength = (paneHeight - windowHeight);
                last = el.position(2);
                if (scrollLength > 0)
                    set(handles.(el.sliderReference).slider,'Enable','on');
                    el.position(2) = el.initPos(2) - (1-slide).*scrollLength;
                else
                    set(handles.(el.sliderReference).slider,'Enable','off');
                    el.position(2) = el.initPos(2);
                end
                update = 0;
                %             disp(['slider : ' num2str(el.position(2)) ' : ' num2str(last) ' : ' num2str(update) ' @ ' datestr(now, 'FFF')]);
            end
            if (update == 1)
                update = 0;
                handles.anchors.(names{i}).update = -1;
            elseif (update == 2)
                update = 0;
                handles.anchors.(names{i}).update = -2;
            end
            if (update == 0)
                pos = el.position;
                if (strcmpi(el.loc,'normalized'))
                    set(el.handle,'Units','normalized');
                    set(el.handle,'Position',[pos(1) pos(2) pos(3) pos(4)]);
                    continue;
                elseif (strcmpi(el.loc,'expand') && pos(1) == 0 && pos(2) == 0 && pos(3) == 0 && pos(4) == 0)
                    set(el.handle,'Units','normalized');
                    set(el.handle,'Position',[0 0 1 1]);
                    continue;
                end
                old_units = get(get(el.handle,'Parent'),'Units');
                set(get(el.handle,'Parent'),'Units','pixels');
                sbar_units = get(el.handle,'Units');
                el.Units='pixels';
                fpos = get(get(el.handle,'Parent'),'Position');
                if (strcmpi(el.loc,'bottom'))
                    upos = [pos(1) + pos(3) pos(2) fpos(3) - 2*(pos(1)) pos(4)];
                elseif (strcmpi(el.loc,'top'))
                    upos = [pos(1) + pos(3) fpos(4) - pos(2) - pos(4) fpos(3) - 2*(pos(1)) pos(4)];
                elseif (strcmpi(el.loc,'left'))
                    upos = [pos(2) pos(1)+pos(3) pos(4) fpos(4) - 2*pos(1)];
                elseif (strcmpi(el.loc,'right'))
                    upos = [fpos(3) - pos(2) - pos(4) pos(1)+pos(3) pos(4) fpos(4) - 2*pos(1)];
                elseif (strcmpi(el.loc,'center'))
                    upos = [(fpos(3) - pos(1))/2 + pos(3) (fpos(4) - pos(2))/2+pos(4) pos(1) pos(2)];
                elseif (strcmpi(el.loc,'expand'))
                    upos = [pos(1) pos(2) fpos(3) - pos(3) - pos(1), fpos(4) - pos(2) - pos(4)];
                else
                    error(['Must specify one of the following locations: Top, Bottom, Left, Right, Center, Expand. Found ' el.loc]);
                end
                mask = upos < 0.1;
                mask(1:2) = 0;
                upos(mask) = 0.1;
                set(el.handle,'Position',upos);
                set(el.handle,'Units',sbar_units);
                set(get(el.handle,'Parent'),'Units',old_units);
            end
        end
        handles.scrollupdate = 0;
        handles.anchors.(names{i}) = el;
        
        numScrolls = sum(cell2mat(strfind(fieldnames(handles),'ScrollPanel')));
        for i = 1:numScrolls
            tmp = get(handles.(['ScrollPanel' num2str(i)]).panel,'Position');
            windowHeight = tmp(4);
            paneHeight = handles.(['ScrollPanel' num2str(i)]).height+25;
            scrollLength = (paneHeight - windowHeight);
            if (scrollLength > 0)
                set(handles.(['ScrollPanel' num2str(i)]).slider,'Enable','on');
            else
                set(handles.(['ScrollPanel' num2str(i)]).slider,'Enable','off');
            end
        end
        %     handles.scrollupdate = 0;
        %     handles.anchors.(names{i}) = el;
    end
    guidata(src,handles);
end