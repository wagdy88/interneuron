import plot_fullCurrents
import plot_fullCurrents_SomaAndProxDend
import comparison_plot

# Run the scripts in sequence
print("Running plot_fullCurrents...")
plot_fullCurrents.main()

print("Running plot_fullCurrents_SomaAndProxDend...")
plot_fullCurrents_SomaAndProxDend.main()

print("Running comparison_plot...")
comparison_plot.main()

print("All scripts completed.")