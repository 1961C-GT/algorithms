function h = uiwaitbar(varargin)
% uiwaitbar  Places/updates a loading bar on a GUI figure
% Init Usage:
%       parent = handles.f;
%       pos = [20 20 200 20];
%       bar = uiwaitbar (parent, pos);
%
% Update Usage:
%       value = 0.8;
%       uiwaitvar(bar, value,'set');
%
% Note that the bar operates with a value of 0 to 1

if (length(varargin) == 3 && strcmpi(varargin{3},'set'))
    ax = varargin{1};
    value = varargin{2};
    p = get(ax,'Child');
    x = get(p,'XData');
    x(3:4) = value;
    set(p,'XData',x)
    return
end

parent = varargin{1};
pos = varargin{2};
bg_color = 'w';
fg_color = [0.0980 0.4745 0.7922];
h = axes('parent',parent,'Units','normalized',...
    'Position',pos,...
    'XLim',[0 1],'YLim',[0 1],...
    'XTick',[],'YTick',[],...
    'Color',bg_color,...
    'XColor',bg_color,'YColor',bg_color);
patch([0 0 0 0],[0 1 1 0],fg_color,...
    'Parent',h,...
    'EdgeColor','none');
end