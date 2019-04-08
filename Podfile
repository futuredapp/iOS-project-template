
platform :ios, '11.4'
swift_version = '5.0'

target '***' do
  # Comment the next line if you're not using Swift and don't want to use dynamic frameworks
  use_frameworks!

  # Funtasty architecture pods
  pod 'FuntastyKit', '~> 1.4'
  pod 'FTAPIKit', '~> 0.4'
  pod 'FTAPIKit', '~> 0.4', subspecs: ['PromiseKit']
  pod 'CellKit', git: 'https://github.com/thefuntasty/CellKit.git', tag: 'v0.2'

  # Third-party pods
  pod 'PromiseKit', '~> 6.0'

  # Tools
  pod 'SwiftLint'

  target '***Tests' do
    inherit! :search_paths
    # Pods for testing
  end
end
