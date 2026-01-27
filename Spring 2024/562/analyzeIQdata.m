function analyzeIQdata(IQdata, options)
    fsample = options.fsample;
    fcarrier = options.fcarrier;



        
    
    switch options.figurePositionsOption
        case 0
            % do nothing
        case 1
            set(0,'units','pixels')
            screenSize = get(0,'ScreenSize');            
            screenHeight = screenSize(4);
            screenWidth = screenSize(3);
            
            
       
            
            lenRatio = 0.30;
            width = round(min(screenHeight,screenWidth)*lenRatio);
            height = width;
            
            xStep = width+5;
            yStep = height+90; 
            
            xrefRatio = 0.55;
            yrefRatio = 0.5;            
            xref = round(screenWidth*xrefRatio);  
            yref = round(screenHeight*yrefRatio);             
                      

            positionRef = [xref,yref,width,height];
        case 2
            options.figureLocationX = 625; % adjust based on your monitor to change the locations of the figures
            options.figureLocationY = 550; % adjust based on your monitor to change the locations of the figures
            % options.figureLocationX = 1925; % adjust based on your monitor to change the locations of the figures
            % options.figureLocationY = 820; % adjust based on your monitor to change the locations of the figures            
            xref = options.figureLocationX;
            yref = options.figureLocationY;
            positionRef = [xref,yref,560,420];
            xStep = 575;
            yStep = 525;
    end

    if (options.showTimeDomainSignal)
        h = figure(1000);
        if options.figurePositionsOption>0
            h.Position = positionRef + [xStep*0,yStep*0,0,0];
        end
        
        subplot(2,1,1)
        plot([0:numel(IQdata)-1]*1/fsample/1e-3, real(IQdata(:)), 'displayname',options.figureName)
        grid on
        hold on    
        title('In-phase')  
        xlabel('Time (ms)')
        ylabel('Amplitude')
        legend('off')
        legend('show')
        legend('Location','Best')  
        ylim([-1 1])

        subplot(2,1,2)
        plot([0:numel(IQdata)-1]*1/fsample/1e-3, imag(IQdata(:)), 'displayname',options.figureName)
        grid on
        hold on    
        title('Quadrature')  
        xlabel('Time (ms)')
        ylabel('Amplitude')
        legend('off')
        legend('show')
        legend('Location','Best')          
        ylim([-1 1])    
    end
    if(options.showPowerSpectralDensity)
        h = figure(1001);
        [valLin,freqList]=pwelch(IQdata,[],[],[],fsample, 'centered');
        plot((freqList+fcarrier)/1e6,10*log10(valLin), 'displayname', options.figureName)
        grid on
        hold on  
        if options.figurePositionsOption>0
            h.Position = positionRef + [xStep*1,yStep*0,0,0];
        end
        xlabel('Frequency (MHz)')
        ylabel('Power/frequency (dB/Hz)')
        title('Power spectral density') 
        legend('off')
        legend('show')  
        legend('Location','Best')  
    end
    if(options.showIQDiagram)
        h = figure(1002);
        if norm(IQdata)>0
            ave = sqrt(mean(maxk((abs(IQdata).^2),10)));
            IQdataN = IQdata/ave;
        else
            IQdataN = IQdata;
            warning('IQdiagram: The power of the signal is 0. Signal is not normalized.')
        end
        plot(real(IQdataN),imag(IQdataN), 'displayname', options.figureName)
        grid on
        hold on 
        if options.figurePositionsOption>0
            h.Position = positionRef + [xStep*1,yStep*-1,0,0];
        end
        xlabel('In-phase')
        ylabel('Quadrature')
        legend('off')
        legend('show')    
        legend('Location','Best')  
        title('IQ diagram (Normalized)')
        drawnow
        maxVal = 1.2;
        xlim([-maxVal maxVal])
        ylim([-maxVal maxVal])
        axis('square')
    end

    if(options.showTimeDomainSignal3D)
        h = figure(1003);
        t = [0:numel(IQdata)-1]*1/fsample/1e-3;
        plot3(t, real(IQdata),imag(IQdata), 'displayname', options.figureName)
        grid on
        hold on  
        if options.figurePositionsOption>0
            h.Position = positionRef + [xStep*0,yStep*-1,0,0];
        end
        xlabel('Time (ms)')
        ylabel('In-phase')
        zlabel('Quadrature')
        legend('off')
        legend('show')    
        legend('Location','Best')  
        title('Time vs. IQ data')
        axis('equal')
        view(gca,[85 3]);
        drawnow
        maxVal = 1.2;
        ylim([-maxVal maxVal])
        zlim([-maxVal maxVal])
    end     
    drawnow
end