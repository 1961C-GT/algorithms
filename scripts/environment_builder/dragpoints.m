function dragpoints(xData,yData)
fh = figure;
x = xData;
y = yData;

ax = axes('xlimmode','manual','ylimmode','manual');
% ax.XLim = [0 30];
% ax.YLim = [0 30];

h = scatter(ax, x,y,'filled','hittest','on','buttondownfcn',@clickmarker);

c = h.CData;
% c is now a 1x3, meaning a RGB color that's used for all of the points
c = repmat(c,[length(x) 1]);
% c is now a 5x3 containing 5 copies of the original RGB
c(1:2,:) = repmat([0 0 1], [2 1]);
c(3:end,:) = repmat([1 0 0], [length(x)-2 1]);
% c now contains red, followed by 4 copies of the original color
h.CData = c;
% Now the scatter object is using those colors
% hold on
% scatter(ax,x+1,y-1,'g*','hittest','on','buttondownfcn',@clickmarker)
% hold off
set(ax, 'Ydir', 'reverse')
grid on; grid minor;
axis(ax, [0 500 0 500]);

ButtonH=uicontrol('Parent',fh,'Style','pushbutton','String','Build CSV','Units','normalized','Position',[0.0 0.5 0.4 0.2],'Visible','on');
% hold off


