%%
clear; clc;


%% Load model results

root = 'Z:\Project_NFWF\3_Modeling\2_xBeach\real_time\Magothy_Bay\output\';
xbo=xb_read_output(root);
xbo2=xbo.data(1).value;

%%

t  = xbo2.data(19).value;
H  = xbo.data(14).value;
zs = xbo.data(10).value;
zb = xbo.data(9).value;
x  = xbo2.data(30).value;
y  = squeeze(xbo2.data(31).value);

%%
baseline=-8;
	index=1:499;
    brown= [0.8 0.8 .6];
    blue2=[0 0.3 1];           
    zs1 = zs(10,:,:);
    zb1 = zb(10,:,:);
    A=figure('units','normalized','outerposition',[0 0 .6 .3]);
        waves = zs(10,1,:) + H(10,1,:);
        A(1)=plot(x,waves,'c'); hold on
        A(2)=plot(x,zs(10,1,:),'b'); hold on
        A(3)=plot(x,zb(10,1,:),'k'); hold on

        A(6)=fill(x(index([ 1 1:end end])),...
               [baseline waves(index) baseline],...
                blue2,'EdgeColor','none'); alpha(.5)                     
        A(7)=fill(x(index([ 1 1:end end])),...
               [baseline zs1(index) baseline],...
               'b','EdgeColor','none'); alpha(.5)                
        A(8)=fill(x(index([1 1:end end])),...
               [baseline zb1(index) baseline],...
               brown,'EdgeColor','none');






%%

for i = 40:41%144
   figure;
    %ax1 = axes;
    %ax2 = axes;
    %linkaxes([ax1,ax2])
    %%Hide the top axes
    %ax2.Visible = 'off';
    %ax2.XTick = [];
    %ax2.YTick = [];
    %c(1) = surf(x,y,squeeze(H(i,:,:))+squeeze(zs(i,:,:))); shading interp;hold on
    c(2) = surf(x,y,squeeze(zb(i,:,:))); shading interp;hold off
    
    %colormap(ax1,'jet')
    colormap('jet')
    %set([ax1,ax2],'Layer', 'top');
end 





%%










%%


%%



%%