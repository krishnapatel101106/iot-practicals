"""
Practical 18 

Aim: Install Windows IoT 10 core on Raspberry pi and run the demo program. 

Hardware Requirements
1. Raspberry Pi 3 Model B/B+ or compatible Raspberry Pi board
2. microSD Card (8 GB or higher)
3. HDMI display and keyboard for initial setup (optional)
4. Windows PC/Laptop
5. Network connection

Software Requirements
1. Windows 10 PC
2. Windows IoT Core image for Raspberry Pi
3. Raspberry Pi-compatible microSD card writing tool
4. Windows IoT Core Dashboard / supported deployment tools
5. Visual Studio with Windows IoT/UWP development support for the demo application


Step 1: Download Windows IoT Core
Download the Windows IoT Core operating-system image and the required tools from Microsoft's
official Windows IoT documentation. Select the image compatible with the Raspberry Pi model
being used. 

Step 2: Prepare the microSD Card. Insert the microSD card into the Windows PC. Use a suitable imaging tool to write the Windows
IoT Core image to the microSD card. After the writing process is completed, safely eject the card.

 Step 3: Insert the microSD Card and Boot Raspberry Pi
1. Insert the prepared microSD card into the Raspberry Pi. 
2. Connect the Raspberry Pi to the network. 
3. Connect the power supply and switch on the Raspberry Pi. 
4. Allow Windows IoT Core to complete its initial boot and configuration. 

Step 4: Connect the Raspberry Pi to the Windows PC
Ensure that the Raspberry Pi and Windows PC are connected to the same network. Identify the
Raspberry Pi on the network and use the Windows IoT management/deployment tools to establish
the connection. 

Step 5: Open the Windows IoT Development Environment
Open Visual Studio on the Windows PC. Create or open a Universal Windows Platform (UWP)
application suitable for Windows IoT Core. Select the Raspberry Pi as the remote target device. 

Step 6: Create the Demo Program
For a simple demonstration, create an application that displays a welcome message and confirms
that the application is running on Windows IoT Core. 

Code:

using Windows.UI.Xaml;
using Windows.UI.Xaml.Controls;

namespace IoTDemo{
    public sealed partial class MainPage : Page{
        public MainPage(){
            this.InitializeComponent();
        }
    }
}

XAML for the Demo Screen
<Page x:Class="IoTDemo.MainPage" 
    xmlns="http://schemas.microsoft.com/winfx/2006/xaml/presentation" 
    xmlns:x="http://schemas.microsoft.com/winfx/2006/xaml">
    <Grid>
        <StackPanel HorizontalAlignment="Center" 
            VerticalAlignment="Center">
        <TextBlock Text="Welcome to Windows IoT Core" 
            FontSize="30" 
            HorizontalAlignment="Center"/>
        <TextBlock Text="Raspberry Pi Demo Program" 
            FontSize="22" 
            Margin="0,20,0,0" 
            HorizontalAlignment="Center"/>
        </StackPanel>
    </Grid>
</Page>

Step 7: Deploy and Run the Demo Program
1. In Visual Studio, select the appropriate target architecture for the Raspberry Pi.
2. Select Remote Machine as the deployment target. 
3. Enter/select the Raspberry Pi device.
4. Build the project. 
5. Deploy and run the application on the Raspberry Pi. 
Output:

+---------------------------------------------------+
|                                                   |
|    Welcome to Windows Iot Core                    |
|                                                   |
|        Raspberry Pi Demo Program                  |
|                                                   |    
+---------------------------------------------------+
"""