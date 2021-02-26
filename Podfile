
platform :ios, '11.4'
swift_version = '5.0'

target '***' do
  # Comment the next line if you're not using Swift and don't want to use dynamic frameworks
  use_frameworks!

  # Funtasty architecture pods
  pod 'FuntastyKit', '~> 1.5'
  pod 'FTAPIKit', '~> 0.5'
  pod 'FTAPIKit', '~> 0.5', subspecs: ['PromiseKit']
  pod 'CellKit', '~> 0.3'

  # Third-party pods
  pod 'PromiseKit', '~> 6.0'

  target '***Tests' do
    inherit! :search_paths
    # Pods for testing
  end
end
